from datetime import datetime
import json
import boto3
from botocore.exceptions import ClientError
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def process(event, context):
    try:
        # Extracting API Key information from the headers. This will be used for metadata definition.  
        # headers = json.loads(event['headers'])
        # if("x-api-key" in headers):
        #     request_origin = headers.get('x-api-key')
        # else:
        #     request_origin = 'unknown'
        
        body = json.loads(event['body'])
        id = str(uuid.uuid4())
        current_timestamp = datetime.now().isoformat()

        item = {
            'id': id,
            'title': body['title'],
            'metadata': {
                'createdAt': current_timestamp,
                'updatedAt': current_timestamp,
                'createdBy': "request_origin",
                'updatedBy': None,
            }
        }
        
        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'body': json.dumps(item),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    
    # Adding validation to check required fields, as required in the challenge specification
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required fields'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
