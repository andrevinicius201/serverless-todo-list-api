from datetime import datetime
import json
import boto3
from botocore.exceptions import ClientError
from util.responses import Responses

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def process(event, context):
    # Extract the id from path parameters
    id = event['path']['id']
    
    # Parse the request body
    body = json.loads(event['body'])
    
    # Prepare the update expression
    update_expression = "SET "
    expression_attribute_values = {}
    for key, value in body.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value
    
    #Get local time in order to update metadata
    current_timestamp = datetime.now().isoformat()
    update_expression+= "updatedAt = :updatedAt"
    expression_attribute_values[":updatedAt"] = current_timestamp
        
    try:
        response = table.update_item(
            Key={'id': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_NEW"
        )
        print(response)
        return responses._201(response['Attributes'])
        
    except ClientError:
        return responses._404({'error': 'Item not found'})
