# reddit-streaming
An attempt to stream api data using kafka, process with spark, and store in s3 data lake.

## Build dockerfiles

Go to docker directory and run build script.

`./build.sh`

`docker-compose up -d --no-recreate`

## Etc.

### Remove untagged docker images

`docker rmi $(docker images | grep "^<none>" | awk "{print $3}")`

### Note on versions

When changing version of spark, hadoop, jupyterlab, etc, versions must be updated in `build.sh`, respective `*.Dockerfile`, `pom.xml`, `requirements.txt` and `reddit_streaming.py`.

### pyspark write stream to s3 error

Likely caused by guava jar mismatch, follow steps here: https://kontext.tech/article/689/pyspark-read-file-in-google-cloud-storage

### Kafka/zookeeper broker id mismatch

https://github.com/wurstmeister/kafka-docker/issues/409

If there are kafka errors, run `docker-compose down`, delete `cluster_config/kafka/logs` and `cluster_config/zookeeper/data/version-2` directories, run `docker-compose up -d`.


## S3

`s3://aws-glue-assets-965504608278-us-east-2/scripts/`

# enhancements

- lambda function to backup s3 to local daily (aws s3 sync...)
- glue function for s3 to docker postgres (aws is $6 a day??? could use a smaller instance?)
- airflow to gracefully restart streaming and producer jobs as needed
- could move from docker-compose local streaming app to cloud based
- kubernetes cluster w/ raspberry pis and local pc