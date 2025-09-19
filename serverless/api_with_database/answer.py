import boto3
import uuid
import json
from datetime import datetime 
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    body = event['body']

    if path == '/vehicles':
        if http_method == 'GET':
            return list_vehicles()
        elif http_method == 'POST':
            return create_vehicle(json.loads(body) if 'body' in event else {})
        elif http_method == 'PUT':
            return update_vehicle(json.loads(body) if 'body' in event else {})

async def create_vehicle(data):
    if not data:
        return {
            'statusCode': 400,
            'body':json.dumps({'error': 'Missing request body'})
        }
    item = {
        'id': str(uuid.uuid4())[:10],
        'record_type': 'vehical',
        'createdAt': datetime.now().isoformat(),
        **data
    }
    await table.put_item(Item=item)
    return {
        'statusCode': 201,
        'body': json.dumps(item)
    }
async def list_vehicles():
    response = await table.query(
        KeyConditionExpression='record_type = :record_type_val',
        ExpressionAttributeValues={':record_type_val': 'vehicle'}
    )
    return{
        'statusCode': 200,
        'body': json.dumps(response.get('Items', []))
    }