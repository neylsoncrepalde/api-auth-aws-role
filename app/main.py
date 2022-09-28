from fastapi import FastAPI
import boto3
from botocore.exceptions import ClientError

sts_client = boto3.client("sts", region_name='us-east-1')

app = FastAPI()

@app.get("/health")
async def root():
    return {
        "statusCode": 200,
        "message": "Vc esta indo muito bem com FastAPI..."
    }

@app.get("/api/{name}")
async def get_user(name):
    return {
        "message": f"Hello, {name} from FastAPI."
    }

@app.get("/comacesso")
async def get_dynamo_com_acesso():
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role_object1=sts_client.assume_role(
        RoleArn="arn:aws:iam::539445819060:role/ROLE_COM_ACESSO_DYNAMO",
        RoleSessionName="AssumeRoleSession1"
    )

    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials1=assumed_role_object1['Credentials']

    dynamo1 = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=credentials1['AccessKeyId'],
        aws_secret_access_key=credentials1['SecretAccessKey'],
        aws_session_token=credentials1['SessionToken']
    )

    response = dynamo1.get_item(
        TableName="tabeladynamo",
        Key={
            "id": {"N": "1"}
        }
    )

    return response


@app.get("/semacesso")
async def get_dynamo_sem_acesso():
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role_object2=sts_client.assume_role(
        RoleArn="arn:aws:iam::539445819060:role/ROLE_SEM_ACESSO_DYNAMO",
        RoleSessionName="AssumeRoleSession1"
    )

    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials2=assumed_role_object2['Credentials']

    dynamo2 = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=credentials2['AccessKeyId'],
        aws_secret_access_key=credentials2['SecretAccessKey'],
        aws_session_token=credentials2['SessionToken']
    )

    try:
        response = dynamo2.get_item(
            TableName="tabeladynamo",
            Key={
                "id": {"N": "1"}
            }
        )
    except ClientError as e:
        return e
    
    return response
