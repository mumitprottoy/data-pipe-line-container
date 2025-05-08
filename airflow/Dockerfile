
FROM apache/airflow:2.9.1-python3.9

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    requests \
    kafka-python

USER airflow

WORKDIR /opt/airflow
