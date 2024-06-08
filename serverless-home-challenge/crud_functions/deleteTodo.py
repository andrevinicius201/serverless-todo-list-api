import json
import boto3
from botocore.exceptions import ClientError
from util.responses import Responses

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()


def process(event, context):
    
    try:
        id = event['path']['id']
    except:
        return responses._400({'error': 'A path must be specified with a todo id'})
        
    try:
        response = table.get_item(Key={'id': id})
        item = response.get('Item')

        if not item:
            return responses._404({'error': 'No TODO item was found with the given ID'})
        
        if not item.get('completed', False):
            return responses._409({'error': 'The Specified TODO item state must be "completed" in order to delete it'})
        
        response = table.delete_item(
            Key={'id': id},
            ConditionExpression="attribute_exists(id) AND completed = :completed",
            ExpressionAttributeValues={":completed": True},
            ReturnValues="ALL_OLD"
        )
        
        return responses._204({'message': 'TODO was deleted successfully', 'todo': response['Attributes']})
        
    
    except ClientError as e:
        return responses._500({'error': 'Internal Server Error'})