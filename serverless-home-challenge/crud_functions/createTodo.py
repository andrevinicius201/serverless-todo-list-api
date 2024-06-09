from datetime import datetime
import json
import boto3
from util.responses import Responses
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()

def process(event, context):
    try:
        title = event['body']['title']
    except KeyError as e:
        return responses._400({'error': 'Missing required fields'})
    
    id = str(uuid.uuid4())
    current_timestamp = datetime.now().isoformat()
    item = {
        'id': id,
        'title': title,
        'completed': False,
        'metadata': {
            'createdAt': current_timestamp,
            'updatedAt': None,
        }
    }

    try:
        response = table.put_item(Item=item)
        return responses._201({'title':title, 'completed': False})
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})
    

    

