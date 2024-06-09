import json
import boto3
from moto import mock_aws
from crud_functions.getTodo import process

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
    Runs a get all operation against an non-existent item
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'zzzzzzz', 'task': 'Complete the serverless home challenge'})

    event = {
        "path": {
            "id": "abcdefgh"
        }
    }

    context = None

    result = process(event, context)
    
    assert result['statusCode'] == 404
    assert result['body'] == {'error': 'No TODO item was found with the given ID'}


@mock_aws
def test_get_data_from_populated_table():
    """
    Runs a get all operation against an existent item
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'})

    event = {
        "path": {
            "id": "abcdefgh"
        }
    }

    context = None

    result = process(event, context)
    
    assert result['statusCode'] == 200
    assert result['body'] == {'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'}


@mock_aws
def test_error_response(mocker):
    """
    Forces an internal server error by trying to get data from a non-existent table
    """

    event = {}
    context = None

    result = process(event, context)

    assert result['body'] == {'error': 'Internal Server Error'}
    assert result['statusCode'] == 500

@mock_aws
def test_unknow_error():
    """
    Forces an internal server error by sending an invalid event payload
    """
    event = {
       "Invalid event payload"
    }

    context = None
    result = process(event, context)
    
    assert result['statusCode'] == 500
    assert result['body'] == {'error': 'Internal Server Error'}