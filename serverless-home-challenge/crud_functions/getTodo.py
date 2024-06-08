import json
import boto3
from util.responses import Responses

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()

def process(event, context):
    try:
        id = event['path']['id']
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})
    
    try:
        response = table.get_item(Key={'id': id})
        
        if 'Item' in response:
            return responses._200(response['Item'])
        else:
            return responses._404({'error': 'No TODO item was found with the given ID'})
        
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})
        