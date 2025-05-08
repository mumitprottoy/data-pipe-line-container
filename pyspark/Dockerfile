FROM bitnami/spark:latest

# Switch to root user to perform package installation
USER root

# Ensure apt-get is up-to-date and clean any cached lists
RUN rm -rf /var/lib/apt/lists/* && apt-get update && apt-get install -y python3-pip python3-venv \
    && pip3 install --upgrade pip \
    && pip3 install \
        jupyter \
        pyspark \
        kafka-python \
        requests \
        pandas

# Set the working directory for Jupyter
WORKDIR /home/notebooks

# Expose ports for Spark and Jupyter
EXPOSE 4040 7077 8888

# Run Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.notebook_dir='/home/notebooks'"]
