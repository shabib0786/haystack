FROM python:3.9 as build

WORKDIR /code

COPY rest_api ./rest_api

# compling the python code
RUN python3 -m compileall -b

FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN python3 -m pip install -r requirements.txt

# Copy REST API code
COPY --from=build code/rest_api /app/rest_api

# making the directory for pyc files
RUN find ./ -type f -name "*.pyc" -exec install -D {} pycFiles/{} \;


EXPOSE 8000
CMD ["gunicorn", "pycFiles.rest_api.application.pyc:app", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "3000"]
