FROM gcr.io/spark-operator/spark-py:v2.4.5

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./jobs/ /opt/spark/jobs/