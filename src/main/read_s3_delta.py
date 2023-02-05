import os
import ast
import logging
import pprint
import yaml
import json
import time
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.column import *
import datetime as dt
import pandas as pd
import numpy as np

import boto3
import pprint
import botocore.session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

def main():
    pp = pprint.PrettyPrinter(indent = 1)
    print("imported modules.")

    # S3 file path
    bucket = "reddit-streaming-stevenhurwitt-new"
    subreddit = "aws"
    filepath = os.path.join("s3a://", bucket, subreddit + "_clean")
    print(filepath)

    # creds.json
    with open("creds.json", "r") as g:
        creds = json.load(g)
        g.close()

    # config.yaml
    with open("config.yaml", "r") as h:
        config = yaml.safe_load(h)
        h.close()

    print("creds.json keys: ")
    pp.pprint([k for k in creds.keys()])

    print("config.yaml keys: ")
    pp.pprint([k for k in config.keys()])

    spark_host = creds["spark_host"]
    spark_port = creds["spark_port"]
    aws_client = creds["aws-access-key"]
    aws_secret = creds["aws-secret-access-key"]
    extra_jar_list = creds["extra_jar_list"]

    # boto3 clients
    s3 = boto3.client("s3")
    athena = boto3.client("athena")
    glue = boto3.client("glue")
    my_lambda = boto3.client("lambda")
    dynamo = boto3.client("dynamodb")
    print("connected to boto3 clients.")

    # spark session
    spark = SparkSession.builder.appName("twitter") \
        .master("spark://{}:{}".format(spark_host, spark_port)) \
        .config("spark.executor.memory", "2048m") \
        .config("spark.executor.cores", "2") \
        .config("spark.streaming.concurrentJobs", "8") \
        .config("spark.local.dir", "/opt/workspace/tmp/driver/") \
        .config("spark.worker.dir", "/opt/workspace/tmp/executor/") \
        .config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", "/opt/workspace/tmp/events/") \
        .config("spark.sql.debug.maxToStringFields", 1000) \
        .config("spark.jars.packages", extra_jar_list) \
        .config("spark.hadoop.fs.s3a.access.key", aws_client) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.buffer.dir", "/opt/workspace/tmp/blocks") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
        .enableHiveSupport() \
        .getOrCreate()

    sc = spark.sparkContext
    # index = 0
    sc.setLogLevel("WARN")
    # sc.setLocalProperty("spark.scheduler.pool", "pool{}".format(str(index)))
    print("imported modules, created spark.")

    # s3 bucket
    bucket_name = "reddit-streaming-stevenhurwitt-new"
    reddit_bucket = s3.list_objects_v2(Bucket = bucket_name)
    for my_bucket_object in reddit_bucket.objects.all():
        print(my_bucket_object.key)

    # athena
    # athena_response = athena.get_query_results(QueryExecutionId = "")
    # print(athena_response)

    # glue
    # glue_response = glue.get_job()
    # print(glue_response)

    # read spark df
    df = spark.read.format("delta").option("header", True).load(filepath)
    df.show()


if __name__ == "__main__":
    main()