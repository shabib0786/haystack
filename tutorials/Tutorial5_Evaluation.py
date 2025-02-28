from haystack import Pipeline
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import (
    ElasticsearchRetriever,
    DensePassageRetriever,
    EmbeddingRetriever,
    EvalAnswers, 
    EvalDocuments,
    FARMReader,
    PreProcessor
)
from haystack.utils import fetch_archive_from_http, launch_es
from haystack.modeling.utils import initialize_device_settings

import logging

logger = logging.getLogger(__name__)


def tutorial5_evaluation():

    ##############################################
    # Settings
    ##############################################
    # Choose from Evaluation style from ['retriever_closed', 'reader_closed', 'retriever_reader_open']
    # 'retriever_closed' - evaluates only the retriever, based on whether the gold_label document is retrieved.
    # 'reader_closed' - evaluates only the reader in a closed domain fashion i.e. the reader is given one query
    #     and one document and metrics are calculated on whether the right position in this text is selected by
    #     the model as the answer span (i.e. SQuAD style)
    # 'retriever_reader_open' - evaluates retriever and reader in open domain fashion i.e. a document is considered
    #     correctly retrieved if it contains the answer string within it. The reader is evaluated based purely on the
    #     predicted string, regardless of which document this came from and the position of the extracted span.
    style = "retriever_reader_open"

    # make sure these indices do not collide with existing ones, the indices will be wiped clean before data is inserted
    doc_index = "tutorial5_docs"
    label_index = "tutorial5_labels"

    ##############################################
    # Code
    ##############################################
    launch_es()
    devices, n_gpu = initialize_device_settings(use_cuda=True)

    # Download evaluation data, which is a subset of Natural Questions development set containing 50 documents
    doc_dir = "../data/nq"
    s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/nq_dev_subset_v2.json.zip"
    fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

    # Connect to Elasticsearch
    document_store = ElasticsearchDocumentStore(
        host="localhost", username="", password="", index="document",
        create_index=False, embedding_field="emb",
        embedding_dim=768, excluded_meta_data=["emb"]
    )

    # Add evaluation data to Elasticsearch document store
    # We first delete the custom tutorial indices to not have duplicate elements
    # and also split our documents into shorter passages using the PreProcessor
    preprocessor = PreProcessor(
        split_by="word",
        split_length=200,
        split_overlap=0,
        split_respect_sentence_boundary=False,
        clean_empty_lines=False,
        clean_whitespace=False
    )
    document_store.delete_documents(index=doc_index)
    document_store.delete_documents(index=label_index)
    document_store.add_eval_data(
        filename="../data/nq/nq_dev_subset_v2.json",
        doc_index=doc_index,
        label_index=label_index,
        preprocessor=preprocessor
    )

    # Let's prepare the labels that we need for the retriever and the reader
    labels = document_store.get_all_labels_aggregated(index=label_index, drop_negative_labels=True, drop_no_answers=False)

    # Initialize Retriever
    retriever = ElasticsearchRetriever(document_store=document_store)

    # Alternative: Evaluate dense Retrievers (DPR and SentenceTransformers)
    # Dense Passage Retrieval uses a separate transformer based encoder for query and document each
    # SentenceTransformers have a single encoder for both
    # Please make sure the "embedding_dim" parameter in the DocumentStore above matches the output dimension of you model
    # Please also take care that the PreProcessor splits your files into chunks that can be completely converted with
    #        the max_seq_len limitations of Transformers
    # The SentenceTransformer model "all-mpnet-base-v2" generelly works well on any kind of english text.
    # For more information check out the documentation at: https://www.sbert.net/docs/pretrained_models.html
    # retriever = DensePassageRetriever(document_store=document_store,
    #                                   query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    #                                   passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    #                                   use_gpu=True,
    #                                   max_seq_len_passage=256,
    #                                   embed_title=True)
    # retriever = EmbeddingRetriever(document_store=document_store, model_format="sentence_transformers",
    #                                embedding_model="all-mpnet-base-v2")
    # document_store.update_embeddings(retriever, index=doc_index)

    # Initialize Reader
    reader = FARMReader(
        model_name_or_path="deepset/roberta-base-squad2",
        top_k=4,
        return_no_answer=True
    )

    # Here we initialize the nodes that perform evaluation
    eval_retriever = EvalDocuments()
    eval_reader = EvalAnswers(sas_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    # Evaluate Retriever on its own in closed domain fashion
    if style == "retriever_closed":
        retriever_eval_results = retriever.eval(top_k=10, label_index=label_index, doc_index=doc_index)
        ## Retriever Recall is the proportion of questions for which the correct document containing the answer is
        ## among the correct documents
        print("Retriever Recall:", retriever_eval_results["recall"])
        ## Retriever Mean Avg Precision rewards retrievers that give relevant documents a higher rank
        print("Retriever Mean Avg Precision:", retriever_eval_results["map"])

    # Evaluate Reader on its own in closed domain fashion (i.e. SQuAD style)
    elif style == "reader_closed":
        reader_eval_results = reader.eval(document_store=document_store, device=devices[0], label_index=label_index, doc_index=doc_index)
        # Evaluation of Reader can also be done directly on a SQuAD-formatted file without passing the data to Elasticsearch
        #reader_eval_results = reader.eval_on_file("../data/nq", "nq_dev_subset_v2.json", device=device)

        ## Reader Top-N-Accuracy is the proportion of predicted answers that match with their corresponding correct answer
        print("Reader Top-N-Accuracy:", reader_eval_results["top_n_accuracy"])
        ## Reader Exact Match is the proportion of questions where the predicted answer is exactly the same as the correct answer
        print("Reader Exact Match:", reader_eval_results["EM"])
        ## Reader F1-Score is the average overlap between the predicted answers and the correct answers
        print("Reader F1-Score:", reader_eval_results["f1"])


    # Evaluate combination of Reader and Retriever in open domain fashion
    elif style == "retriever_reader_open":

        # Here is the pipeline definition
        p = Pipeline()
        p.add_node(component=retriever, name="Retriever", inputs=["Query"])
        p.add_node(component=eval_retriever, name="EvalDocuments", inputs=["Retriever"])
        p.add_node(component=reader, name="Reader", inputs=["EvalDocuments"])
        p.add_node(component=eval_reader, name="EvalAnswers", inputs=["Reader"])
        results = []

        for l in labels:
            res = p.run(
                query=l.query,
                labels=l,
                params={"index": doc_index, "Retriever": {"top_k": 10}, "Reader": {"top_k": 5}},
            )
            results.append(res)

        eval_retriever.print()
        print()
        retriever.print_time()
        print()
        eval_reader.print(mode="reader")
        print()
        reader.print_time()
        print()
        eval_reader.print(mode="pipeline")
    else:
        raise ValueError(f'style={style} is not a valid option. Choose from retriever_closed, reader_closed, retriever_reader_open')


if __name__ == "__main__":
    tutorial5_evaluation()

# This Haystack script was made with love by deepset in Berlin, Germany
# Haystack: https://github.com/deepset-ai/haystack
# deepset: https://deepset.ai/