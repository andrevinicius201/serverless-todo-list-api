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
        item = response.get('Item')

        if not item:
            return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'No TODO item was found with the given ID'}),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                }
        
        
        if not item.get('completed', False):
            return {
                'statusCode': 409,
                'body': json.dumps({'error': 'The Specified TODO item state must be "completed" in order to delete it'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        delete_response = table.delete_item(
            Key={'id': id},
            ConditionExpression="attribute_exists(id) AND completed = :completed",
            ExpressionAttributeValues={":completed": True},
            ReturnValues="ALL_OLD"
        )
    
        return {
                'statusCode': 201,
                'body': json.dumps({'message': 'TODO was deleted successfully', 'todo': delete_response.get('Attributes')}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
