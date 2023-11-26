FROM apache/spark-py:v3.4.0

COPY requirements.txt ./
USER root
RUN pip3 install -r ./requirements.txt

COPY ./src /opt/spark/jobs/
