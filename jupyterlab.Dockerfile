FROM cluster-base
FROM continuumio/anaconda3:2020.11

# -- Layer: Python

# set args
ARG spark_version=3.3.2
ARG jupyterlab_version=3.5.2

# copy dependencies
COPY ./notebooks/ ${SHARED_WORKSPACE}/aws/notebooks/
COPY ./src ${SHARED_WORKSPACE}/aws/src
COPY ./env/requirements.txt ${SHARED_WORKSPACE}/aws/requirements.txt
COPY ./env/aws.yml ${SHARED_WORKSPACE}/aws/aws.yml

# base python
RUN apt-get --allow-releaseinfo-change update && \
    apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y python3-dev python3-distutils python3-setuptools python3-venv

RUN curl https://bootstrap.pypa.io./get-pip.py | python3 && \
    python3 -m pip install --upgrade pip

# virtualenv - pip venv
RUN python3 -m venv /opt/workspace/reddit-env 
    # && \
    # source /opt/workspace/reddit-env/bin/activate

# pyspark & jupyterlab - pip (old)
RUN pip3 install pyspark==${spark_version} jupyterlab==${jupyterlab_version}

# -- Layer: Conda Environment

# pyspark & jupyterlab - conda
# RUN conda install -c conda-forge pyspark==${spark_version} jupyterlab==${jupyterlab_version}

# custom .whl's - pip (old)
# RUN pip3 install /opt/workspace/redditStreaming/src/main/python/reddit/dist/reddit-0.1.0-py3-none-any.whl --force-reinstall

# requirements - pip (old)
RUN pip3 install -r /opt/workspace/src/requirements.txt --ignore-installed

# create conda env
# RUN conda --help
# RUN conda env create -n aws -f env/aws.yml

# add kernel to jupyter
# RUN python3 -m ipykernel install --user --name="aws"
    
# -- Layer: aws-cli

# aws
RUN rm -rf /var/lib/apt/lists/* && \
    mkdir root/.aws
    # aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID} && \
    # aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
    # ln -s /usr/local/bin/python3 /usr/bin/python

# -- Layer: Outdated Guava JAR File

# this is fixed!!! yay
# feel free to ignore commented code below:
# 
# deal w/ outdated pyspark guava jar for hadoop-aws (check maven repo for hadoop-common version)
# RUN cd /usr/local/lib/python3.7/dist-packages/pyspark/jars/ && \
#     rm guava-14.0.1.jar && \
#     wget https://repo1.maven.org/maven2/com/google/guava/guava/31.1-jre/guava-31.1-jre.jar


# -- Runtime
EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}/aws
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=easy --NotebookApp.password=easy --notebook-dir=${SHARED_WORKSPACE}

