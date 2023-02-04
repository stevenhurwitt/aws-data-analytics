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
    "aws-secret-access-key": ""
}
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