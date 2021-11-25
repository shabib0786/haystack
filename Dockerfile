FROM python:3.7.4-stretch as build

WORKDIR /code

COPY rest_api ./rest_api

# compling the python code
RUN python -m compileall -b

FROM python:3.7.4-stretch

WORKDIR /app

RUN apt-get update && apt-get install -y curl git pkg-config cmake

# Install PDF converter
RUN wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.03.tar.gz && \
    tar -xvf xpdf-tools-linux-4.03.tar.gz && cp xpdf-tools-linux-4.03/bin64/pdftotext /usr/local/bin

RUN apt-get install libpoppler-cpp-dev pkg-config -y --fix-missing

# Install Tesseract
RUN apt-get install tesseract-ocr libtesseract-dev poppler-utils -y

# install as a package ->setup.py
COPY requirements.txt README.md /app/
RUN pip install -r requirements.txt

# Copy REST API code
COPY --from=build code/rest_api /app/rest_api

# making the directory for pyc files
RUN find ./ -type f -name "*.pyc" -exec install -D {} pycFiles/{} \;


EXPOSE 8000
CMD ["gunicorn", "pycFiles.rest_api.application.pyc:app", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "3000"]


# # Copy REST API code
# COPY rest_api /app/rest_api

# optional : copy sqlite db if needed for testing
#COPY qa.db /home/user/

# optional: copy data directory containing docs for ingestion
#COPY data /home/user/data

# cmd for running the API
# CMD ["gunicorn", "rest_api.application:app",  "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "3000"]

# RUN pip install -e .

# copy saved models
# COPY README.md models* /home/user/models/


