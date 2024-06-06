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
def testUpdateExistingItemValidPayload():
    """
    Updates existing todo item
    """
    table = setup_dynamodb_table()

    table.put_item(Item={'id': 'abcdefgh', 'title': 'Complete AWS home challenge'})
    
    update_item_status_event = {
        'pathParameters': {"id": "abcdefgh"},
        'body': '{\r\n    "completed":true\r\n}\r\n',
    }
    
    update_item_status_context = None
    result = crud_functions.updateTodo.process(update_item_status_event, update_item_status_context)
    
    assert result['statusCode'] == 201
    assert json.loads(result['body'])["completed"] == True
    assert result['headers']['Content-Type'] == 'application/json'
    assert result['headers']['Access-Control-Allow-Origin'] == '*'

@mock_aws 
def testUpdateNotExistingItem():
    table = setup_dynamodb_table()
    
    update_item_status_event = {
        'pathParameters': {"id": "abcdefgh"},
        'body': '{\r\n    "completed":true\r\n}\r\n',
    }
    
    update_item_status_context = None
    result = crud_functions.updateTodo.process(update_item_status_event, update_item_status_context)
    assert result['statusCode'] == 404
    assert json.loads(result['body']) == {"error": "Item not found"}


@mock_aws
def testUpdateExistingItemInvalidPayload():
    pass


