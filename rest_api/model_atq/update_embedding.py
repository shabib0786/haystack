from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.retriever.dense import DensePassageRetriever
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.preprocessor import PreProcessor
import sys

document_store_atq = ElasticsearchDocumentStore(host='localhost', username="", password="",
                            index="nsl_support_document_atq",
                            embedding_dim=768
                                )

doc_dir = "document"

all_docs = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
#print(all_docs)update_existing_embeddings=False
processor = PreProcessor(clean_empty_lines=True,
                        clean_whitespace=True,
                        clean_header_footer=True,
                        split_by="word",
                        split_length=200,
                        split_respect_sentence_boundary=True,
                        split_overlap=0
                        )
docs = processor.process(all_docs)


#document_store_atq.delete_documents(index="nsl_support_document_atq")
document_store_atq.write_documents(docs,index="nsl_support_document_atq")

retriever_atq = DensePassageRetriever(document_store=document_store_atq, 
                    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                    use_gpu = False)


document_store_atq.update_embeddings(retriever=retriever_atq,index="nsl_support_document_atq",update_existing_embeddings=False)
