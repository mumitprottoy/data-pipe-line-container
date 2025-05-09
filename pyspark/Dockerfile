FROM bitnami/spark:3.5.1

USER root

# Install Python 3.11 and curl
RUN apt-get update && \
    apt-get install -y python3.11 python3.11-distutils curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Copy requirements and notebooks
COPY requirements.txt /app/requirements.txt
COPY notebooks /app/notebooks

# Install Python packages
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install -r /app/requirements.txt

# Set environment variable for Spark JARs directory
ENV SPARK_JARS_DIR="/opt/bitnami/spark/jars"

# Download required Kafka integration JARs for Spark 3.5.1 (Scala 2.12)
RUN curl -L -o $SPARK_JARS_DIR/spark-sql-kafka-0-10_2.12-3.5.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar && \
    curl -L -o $SPARK_JARS_DIR/spark-token-provider-kafka-0-10_2.12-3.5.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.1/spark-token-provider-kafka-0-10_2.12-3.5.1.jar && \
    curl -L -o $SPARK_JARS_DIR/kafka-clients-3.5.1.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.1/kafka-clients-3.5.1.jar && \
    curl -L -o $SPARK_JARS_DIR/commons-pool2-2.11.1.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
    curl -L -o $SPARK_JARS_DIR/lz4-java-1.8.0.jar \
      https://repo1.maven.org/maven2/org/lz4/lz4-java/1.8.0/lz4-java-1.8.0.jar

# Download MySQL JDBC connector
RUN curl -L -o $SPARK_JARS_DIR/mysql-connector-java-8.0.33.jar \
      https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar

WORKDIR /app
