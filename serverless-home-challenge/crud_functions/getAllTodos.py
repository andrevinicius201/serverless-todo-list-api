import json
import boto3
from util.responses import Responses
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()

def process(event, context):
    
    try:
        response = table.scan()
        data = response['Items'] if response['Items'] else []
        return responses._200(data)
        
    except ClientError as e:
        return responses._404({'error': str(e)})