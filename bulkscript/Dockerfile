FROM ubuntu:latest

WORKDIR /bulkscript

COPY ./bulk_upload.py /bulkscript/bulk_upload.py
COPY ./top250-00-19.csv /bulkscript/top250-00-19.csv
COPY ./requirements.txt  /bulkscript/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt 

EXPOSE 8000

CMD ["python3","bulk_upload.py"]