# aws-data-analytics
aws data analytics study guide (DAS-C01) for boto3 python client.

## local `creds.json` file

- create `creds.json` file like so:
- `creds.json`:
```json
{
    "twitter-api-key": "",
    "twitter-secret-key": "",
    "twitter-bearer": "",
    "twitter-access-token": "",
    "twitter-secret-access": "",
    "aws-access-key": "",
    "aws-secret-access-key": "",
    "spark_host": "spark-master",
    "spark_port": "7077",
    "dynamo_host": "xanaxprincess.asuscomm.com",
    "dynamo_port": "8000",
    "extra_jar_list": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.apache.hadoop:hadoop-common:3.3.4,org.apache.hadoop:hadoop-aws:3.3.4,org.apache.hadoop:hadoop-client:3.3.4,io.delta:delta-core_2.12:2.2.0,org.postgresql:postgresql:42.5.0"
}
```

again, these are the keys:

```python
['twitter-api-key',
 'twitter-secret-key',
 'twitter-bearer',
 'twitter-access-token',
 'twitter-secret-access',
 'aws-access-key',
 'aws-secret-access-key',
 'spark_host',
 'spark_port',
 'dynamo_host',
 'dynamo_port',
 'extra_jar_list']
```

get twitter api key/secrets from twitter developer portal.

get aws access/secret keys from aws console for iam user.

## aws configure

- install `aws-cli`
- `aws configure`

need aws access key/secret from console. can regenerate if needed. enable secret rotation lambda??

## python - boto3

- install `python3`, `pip`, `setuptools`, `wheel`
- `pip install -r requirements.txt`

install python dependencies. can create conda env as well:

- `conda env create -f env/twitter.yml`

this will created version controlled environment files for pip/conda.

# to-do

... in no particular order...

- `main.py` updates and modifications
- CI/CD w/ concourse??
- github actions
- py envs!
- docker build
    - dynamo
    - postgres
    - pyspark
    - kafka
    - jupyterlab
- docker-compose up -d