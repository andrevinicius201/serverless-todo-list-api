import json
import boto3
from botocore.exceptions import ClientError
from util.responses import Responses
import jwt

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')
responses = Responses()


def process(event, context):

    try:
        token = event['headers'].get('Authorization').split()[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_role = decoded_token['cognito:groups'][0]
        if(user_role != "administrator"):
            return responses._403({'error': 'Only administrators can delete all TODOs'})
    except:
        return responses._403({'error': '"Authorization" header was not provided or it is incorrectly formatted'})
    
    try:
        response = table.scan()
        data = response['Items']

        with table.batch_writer() as batch:
            for item in data:
                batch.delete_item(
                    Key={
                        'id': item['id']
                    }
                )

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data = response['Items']

            with table.batch_writer() as batch:
                for item in data:
                    batch.delete_item(
                        Key={
                            'id': item['id']
                        }
                    )
            
        return responses._204({'message': 'All table items were deleted successfully'})
          
    except Exception as e:
        return responses._500({'error': 'Internal Server Error'})