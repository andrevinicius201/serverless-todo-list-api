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

    event = {}
    event['body'] = {"title":"Fix the car engine"}    

    context = None

    result = process(event, context)
    assert result['statusCode'] == 201
    assert result['body'] == {'title':'Fix the car engine', 'completed':False}

@mock_aws
def testAddTodoInvalidPayloadMissingField():
    """
    Tries to add a new item in the table with an invalid payload (sending 'task_name' instead 'title') so that the input does not match the required schema.
    """
    table = setup_dynamodb_table()

    event = {}
    event['body'] = {"task_name":"Fix the car engine"} 
    context = None

    result = process(event, context)
    assert result['statusCode'] == 400
    assert result['body'] == {'error': 'Missing required fields'}


@mock_aws
def test_error_response():
    """
    Forces an internal server error by trying to populate an non-existent table.
    """

    event = {}
    event['body'] = {"title":"Fix the car engine"} 
    context = None

    result = process(event, context)
    assert result['statusCode'] == 500
    assert result['body'] == {'error': 'Internal Server Error'}

