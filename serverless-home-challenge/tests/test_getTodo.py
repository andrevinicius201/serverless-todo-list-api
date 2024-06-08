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
    Runs a get all operation against an item that not exists
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
    assert result['body'] == {'error': 'TO-DO item was not found'}


@mock_aws
def test_get_data_from_populated_table():
    """
    Runs a get all operation against an existing item
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
def test_unknow_error():
    """
    Tests an unknown error situation
    """
    event = {
       "Invalid event payload"
    }

    context = None
    result = process(event, context)
    
    assert result['statusCode'] == 500
    assert result['body'] == {'error': 'Internal Server Error'}