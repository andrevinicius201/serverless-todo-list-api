import json
import boto3
from moto import mock_aws
from crud_functions.getAllTodos import process
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
def test_get_data_from_empty_table():
    """
    Runs a get all operation against am empty todos table
    """
    table = setup_dynamodb_table()

    event = {}
    context = None

    result = process(event, context)
    
    assert result['statusCode'] == 200
    assert result['body'] == []


@mock_aws
def test_get_data_from_populated_table():
    """
    Runs a get all operation agains a table with 3 todo items
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': '1', 'task': 'Complete the serverless home challenge'})
    table.put_item(Item={'id': '2', 'task': 'Get an interview'})
    table.put_item(Item={'id': '3', 'task': 'Get an job offer'})

    event = {}
    context = None

    result = process(event, context)
    body = result['body']

    assert result['statusCode'] == 200
    assert len(body) == 3
    assert {'id': '1', 'task': 'Complete the serverless home challenge'} in body
    assert {'id': '2', 'task': 'Get an interview'} in body
    assert {'id': '3', 'task': 'Get an job offer'} in body


@mock_aws
def test_client_error_response(mocker):
    mocker.patch('boto3.resource', side_effect=ClientError(
        error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Requested resource not found'}},
        operation_name='scan'
    ))

    event = {}
    context = None

    result = process(event, context)

    assert result['body'] == {"error": "An error occurred (ResourceNotFoundException) when calling the Scan operation: Requested resource not found"}
    assert result['statusCode'] == 404
