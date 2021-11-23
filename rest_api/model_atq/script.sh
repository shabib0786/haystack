#!/bin/sh
host=${1}

echo "Do you want to train the model?(y/n) "
read VAR

echo "Enter the document path"
    read document
    cp $document ./document

if [[ $VAR -eq "y" || $VAR -eq "Y" ]]
then
    echo "Enter the QnA file path"
    read QnA
    echo "enter the model name"
    read model_name
    cp $QnA ./answers.json
    python3 train.py $model_name 
    python3 update_embedding.py $host 
else
    python3 update_embedding.py $host
fi








