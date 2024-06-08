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
        # Extracting API Key information from the headers. This will be used for metadata definition.  
        # headers = json.loads(event['headers'])
        # if("x-api-key" in headers):
        #     request_origin = headers.get('x-api-key')
        # else:
        #     request_origin = 'unknown'
        
        title = event['body']['title']
    # Adding validation to check required fields, as required in the challenge specification
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
            'updatedAt': current_timestamp,
            'createdBy': "request_origin",
            'updatedBy': None,
        }
    }

    try:
        response = table.put_item(Item=item)
        return responses._201({'title':title, 'completed': False})
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})
    

    

