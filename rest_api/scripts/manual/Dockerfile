FROM python:3.7.4-stretch



WORKDIR /script

USER root



COPY requirements.txt .

RUN pip install -r requirements.txt

# RUN python -m pip install --upgrade pip

# RUN pip3 install farm-haystack

COPY ${filepath} ${filepath}

# COPY ${filepath} ./data.csv

COPY elastic-script .

RUN pwd

RUN ls -lrt





# USER root

# RUN apt-get install python3-pip



# RUN python3 -m pip install --upgrade pip

# RUN pip install -r /script/requirements.txt



CMD ["sh", "-c","/script/elastic-script --filepath=${filepath} --elasticip=${elasticip} --esport=${esport}"]