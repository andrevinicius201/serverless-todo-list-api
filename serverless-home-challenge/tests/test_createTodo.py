import json
import boto3
from moto import mock_aws
from crud_functions.createTodo import process
from botocore.exceptions import ClientError

@mock_aws
def setup_dynamodb_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='todos',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='todos')
    return table

@mock_aws
def testAddTodoValidPayload():
    """
    Adds a new todo item in the table
    """
    table = setup_dynamodb_table()

    event = {
        'body': '{\r\n "title":"Fix the car engine"\r\n}\r\n', 
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 201
    assert json.loads(result['body'])['title'] == 'Fix the car engine'
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['headers']['Access-Control-Allow-Origin'] == '*'

@mock_aws
def testAddTodoInvalidPayload():
    """
    Tries to add a new item in the table with an invalid payload (sending 'task_name' instead 'title'). Input does not match the required schema.
    """
    table = setup_dynamodb_table()

    event = {
        'body': '{\r\n "task_name":"Fix the car engine"\r\n}\r\n', 
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 400
    assert json.loads(result['body'])['error'] == 'Missing required fields'
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['headers']['Access-Control-Allow-Origin'] == '*'

