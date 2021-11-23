from haystack.reader.farm import FARMReader

reader = FARMReader(model_name_or_path='deepset/roberta-base-squad2') 
reader.train(data_dir=".", train_filename="answers.json", use_gpu=True, n_epochs=1, save_dir="my_model")

reader.save(directory="my_model")
