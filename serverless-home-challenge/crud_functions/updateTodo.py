from datetime import datetime
import json
import boto3
from botocore.exceptions import ClientError
from util.responses import Responses

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def process(event, context):
    
    try:
        id = event['path']['id']
        body = event['body']

        update_expression = "SET "
        expression_attribute_values = {}
        for key, value in body.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
        
        current_timestamp = datetime.now().isoformat()
        update_expression+= "updatedAt = :updatedAt"
        expression_attribute_values[":updatedAt"] = current_timestamp
    
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})
        
    try:
        response = table.update_item(
            Key={'id': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_NEW"
        )
        return responses._201(response['Attributes'])
        
    except ClientError:
        return responses._404({'error': 'No TODO item was found with the given ID'})
