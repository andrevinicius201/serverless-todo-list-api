import json
import boto3
from moto import mock_aws
from crud_functions.deleteTodo import process
from crud_functions import updateTodo
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
def testDeleteTodoNotCompletedItem():
    """
    Tries to delete an item before it is set under "completed" status
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
    assert result['statusCode'] == 409
    assert result['body'] == {'error': 'The Specified TODO item state must be "completed" in order to delete it'}

@mock_aws
def testDeleteTodoNotExistentItem():
    """
    Tries to delete an item using a not existent item id
    """
    table = setup_dynamodb_table()

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
def testDeleteTodoExistingItem():
    """
    Deletes successfully an item from the table
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'})

    update_item_status_event = {
        'path': {
            'id': 'abcdefgh'
        },
        'body': {"completed":True}
    }
    update_item_status_context = None
    updateTodo.process(update_item_status_event, update_item_status_context)
    event = {
        "path": {
            "id": "abcdefgh"
        }
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 204