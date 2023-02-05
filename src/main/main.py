from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.column import *
import pandas as pd
import numpy as np
import pprint
import boto3
import time
import json
import ast
import os


def get_aws_session():
    session = boto3.session.Session()
    return session

def get_aws_client(service, region):
    session = get_aws_session()
    client = session.client(service, region_name=region)
    return client
    
def get_aws_resource(service, region):
    session = get_aws_session()
    resource = session.resource(service, region_name=region)
    return resource

def get_aws_account_id():
    client = get_aws_client('sts', 'us-east-1')
    return client.get_caller_identity().get('Account')

def get_aws_account_alias():
    client = get_aws_client('iam', 'us-east-1')
    return client.list_account_aliases().get('AccountAliases')[0]

def get_aws_regions():
    client = get_aws_client('ec2', 'us-east-1')
    return [region['RegionName'] for region in client.describe_regions().get('Regions')]

def main():
    """
    Main function
    """
    start = time.time()
    base = os.getcwd()

    account_id = get_aws_account_id()
    account_alias = get_aws_account_alias()
    regions = get_aws_regions()
    print("Account ID: {}".format(account_id))
    print("Account Alias: {}".format(account_alias))
    print("Regions: {}".format(regions))

    dynamo = get_aws_client('dynamodb', 'us-east-1')
    s3 = get_aws_client('s3', 'us-east-2')
    glue = get_aws_client('glue', 'us-east-2')
    my_lambda = get_aws_client('lambda', 'us-east-2')
    # lambda = get_aws_client('lambda', 'us-east-2')

    # Create DynamoDB table
    dynamo.create_table(
        TableName='test',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Create S3 bucket
    s3.create_bucket(
        Bucket='test',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2'
        }
    )
    
    # Create Glue Crawler
    glue.create_crawler(
        Name='test',
        Role='arn:aws:iam::{}:role/service-role/AWSGlueServiceRole-test'.format(account_id),
        DatabaseName='test',
        Targets={
            'S3Targets': [
                {
                    'Path': 's3://test/'
                }
            ]
        }
    )

    # Create Lambda function
    my_lambda.create_function(
        FunctionName='test',
        Runtime='python3.9',
        Role='arn:aws:iam::{}:role/service-role/AWSLambdaBasicExecutionRole-test'.format(account_id),
        Handler='main.lambda_handler',
        Code={
            'ZipFile': open(base + '/lambda.zip', 'rb').read()
        },
        Timeout=3,
        MemorySize=128,
        Publish=True
    )

    # Invoke Lambda function
    my_lambda.invoke(
        FunctionName='test',
        InvocationType='Event',
        Payload=json.dumps({
            'test': 'test'
        })
    )

    end = time.time()
    print("Total time: {}".format(end - start))
    return(None)


if __name__ == '__main__':
    main()