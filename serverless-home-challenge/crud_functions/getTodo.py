import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def process(event, context):
    try:
        id = event['pathParameters']['id']
    except:
        return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'A path must be specified with a todo id'
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
        }
    
    try:
        response = table.get_item(Key={'id': id})
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item']),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'TO-DO item was not found'
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }