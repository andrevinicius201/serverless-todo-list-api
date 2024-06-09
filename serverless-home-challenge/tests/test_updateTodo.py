import json
import boto3
from moto import mock_aws
import crud_functions.createTodo
import crud_functions.updateTodo
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
def testUpdateExistentItem():
    """
    Updates existing todo item
    """
    table = setup_dynamodb_table()

    table.put_item(Item={'id': 'abcdefgh', 'title': 'Complete AWS home challenge'})
    
    update_item_status_event = {
        'path': {"id": "abcdefgh"},
        'body': {"completed":True}
    }
    
    update_item_status_context = None
    result = crud_functions.updateTodo.process(update_item_status_event, update_item_status_context)
    
    assert result['statusCode'] == 201
    assert result['body']['title'] == 'Complete AWS home challenge'
    assert result['body']['completed'] == True

@mock_aws 
def testUpdateNotExistentItem():
    """
    Tries to update a non-existent todo item
    """
    table = setup_dynamodb_table()
    
    update_item_status_event = {
        'path': {"id": "abcdefgh"},
        'body': {"completed":True}
    }
    
    update_item_status_context = None
    result = crud_functions.updateTodo.process(update_item_status_event, update_item_status_context)
    assert result['statusCode'] == 404
    assert result['body'] == {"error": "No TODO item was found with the given ID"}

@mock_aws
def test_unknow_error():
    """
    Forces an internal server error by sending an invalid event payload
    """
    event = {
       "Invalid event payload"
    }

    context = None
    result = crud_functions.updateTodo.process(event, context)
    
    assert result['statusCode'] == 500
    assert result['body'] == {'error': 'Internal Server Error'}



