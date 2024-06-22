FROM python:3.8-slim-buster
RUN pip install deepdiff pymongo
RUN mkdir /app
COPY library/ /app/library/
COPY PythonScript.py /app/PythonScript.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "PythonScript.py" ]
