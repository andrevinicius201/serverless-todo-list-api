import json
import boto3
from moto import mock_aws
from crud_functions.deleteAllTodos import process
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
def testDeleteTodoExistingItem():
    """
    Deletes successfully an item from the table
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'})
    table.put_item(Item={'id': 'fghijkij', 'task': 'Clean the kitchen'})
    

    event = {
        'headers': {
            'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiAiYjQyODQ0MTgtMTAyMS03MGI3LTljZjQtNjYyMzM0NjhhMzQzIiwgImNvZ25pdG86Z3JvdXBzIjogWyJhZG1pbmlzdHJhdG9yIl0sICJpc3MiOiAiaHR0cHM6Ly9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbS91cy1lYXN0LTFfd0Z0VDlpT2ZUIiwgInZlcnNpb24iOiAyLCAiY2xpZW50X2lkIjogIjFwaDlscnRubjhhZWFrM3ZtbWY2ajYxYTJjIiwgImV2ZW50X2lkIjogIjM3MDAyNDc4LWU2YjYtNDZjMS1hODYzLWY4OTM0YmI3NGE4OCIsICJ0b2tlbl91c2UiOiAiYWNjZXNzIiwgInNjb3BlIjogInBob25lIG9wZW5pZCBlbWFpbCIsICJhdXRoX3RpbWUiOiAxNzE3ODY3NzAyLCAiZXhwIjogMTcxNzg3MTMwMiwgImlhdCI6IDE4OTMyNTUyNTAsICJqdGkiOiAiMDA5MmJlMjQtNmNhZS00MzE0LTljYzctMmJlM2VkNWQ1MTdkIiwgInVzZXJuYW1lIjogImFuZHZpbmkifQ.HGSlm2B1fi-ZOE8M9yb_pQtw7Sp8KDhuZ_4lf1XzHhY'
        }
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 204

@mock_aws
def testDeleteTodosAsGeneralUser():
    """
    Deletes successfully an item from the table
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'})
    table.put_item(Item={'id': 'fghijkij', 'task': 'Clean the kitchen'})
    

    event = {
        'headers': {
            'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNDI4NDQxOC0xMDIxLTcwYjctOWNmNC02NjIzMzQ2OGEzNDMiLCJjb2duaXRvOmdyb3VwcyI6WyJnZW5lcmFsIl0sImlzcyI6Imh0dHBzOi8vY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb20vdXMtZWFzdC0xX3dGdFQ5aU9mVCIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjFwaDlscnRubjhhZWFrM3ZtbWY2ajYxYTJjIiwiZXZlbnRfaWQiOiIzNzAwMjQ3OC1lNmI2LTQ2YzEtYTg2My1mODkzNGJiNzRhODgiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6InBob25lIG9wZW5pZCBlbWFpbCIsImF1dGhfdGltZSI6MTcxNzg2NzcwMiwiZXhwIjoxNzE3ODcxMzAyLCJpYXQiOjE4OTMyNTUyNTAsImp0aSI6IjAwOTJiZTI0LTZjYWUtNDMxNC05Y2M3LTJiZTNlZDVkNTE3ZCIsInVzZXJuYW1lIjoiYW5kdmluaSJ9.DE2_UgMasxSR1rcisjJpYQ7VJv4zMY1OfCopClQ1ZK0'
        }
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 403
    assert result['body'] == {'error': 'Only administrators can delete all TODOs'}

@mock_aws
def testDeleteTodosInvalidAccessToken():
    """
    Deletes successfully an item from the table
    """
    table = setup_dynamodb_table()
    table.put_item(Item={'id': 'abcdefgh', 'task': 'Complete the serverless home challenge'})
    table.put_item(Item={'id': 'fghijkij', 'task': 'Clean the kitchen'})
    

    event = {
        'headers': {
            'Authorization': 'Bearer test'
        }
    }
    context = None

    result = process(event, context)
    assert result['statusCode'] == 403
    assert result['body'] == {'error': '"Authorization" header was not provided or it is incorrectly formatted'}


