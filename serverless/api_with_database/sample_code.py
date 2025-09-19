# AWS SDK for Python (Boto3) - https://aws.amazon.com/sdk-for-python/
import json
import os
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB client
# Boto3 - DynamoDB - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    """
    Lambda handler for processing API Gateway requests
    """
    http_method = event['httpMethod']
    path = event['path']
    
    # Route the request based on path and method
    if path == '/vehicles':
        if http_method == 'GET':
            return list_vehicles()
        elif http_method == 'POST':
            return create_vehicle(json.loads(event['body']) if 'body' in event else {})
        elif http_method == 'PUT':
            return update_vehicle(json.loads(event['body']) if 'body' in event else {})
    elif path == '/locations':
        if http_method == 'GET':
            return list_locations()
        elif http_method == 'POST':
            return create_location(json.loads(event['body']) if 'body' in event else {})
        elif http_method == 'PUT':
            return update_location(json.loads(event['body']) if 'body' in event else {})
    
    # Default response for unhandled routes
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found'})
    }

# Vehicle handlers
def create_vehicle(data):
    if not data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing request body'})
        }
    
    item = {
        'id': str(uuid.uuid4())[:10],
        'record_type': 'vehicle',
        'createdAt': datetime.now().isoformat(),
        **data
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 201,
        'body': json.dumps(item)
    }

def update_vehicle(data):
    if not data or 'id' not in data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing id in request body'})
        }
    
    item_id = data['id']
    update_expression = 'SET updatedAt = :updatedAt'
    expression_values = {
        ':updatedAt': datetime.now().isoformat()
    }
    
    # Build update expression dynamically
    for key, value in data.items():
        if key != 'id':
            update_expression += f', {key} = :{key}'
            expression_values[f':{key}'] = value
    
    table.update_item(
        Key={
            'id': item_id,
            'record_type': 'vehicle'
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'id': item_id, 'message': 'Vehicle updated successfully'})
    }

def list_vehicles():
    response = table.query(
        KeyConditionExpression='record_type = :record_type_val',
        ExpressionAttributeValues={':record_type_val': 'vehicle'}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Items', []))
    }

# Location handlers
def create_location(data):
    if not data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing request body'})
        }
    
    item = {
        'id': str(uuid.uuid4())[:10],
        'record_type': 'location',
        'createdAt': datetime.now().isoformat(),
        **data
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 201,
        'body': json.dumps(item)
    }

def update_location(data):
    if not data or 'id' not in data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing id in request body'})
        }
    
    item_id = data['id']
    update_expression = 'SET updatedAt = :updatedAt'
    expression_values = {
        ':updatedAt': datetime.now().isoformat()
    }
    
    # Build update expression dynamically
    for key, value in data.items():
        if key != 'id':
            update_expression += f', {key} = :{key}'
            expression_values[f':{key}'] = value
    
    table.update_item(
        Key={
            'id': item_id,
            'record_type': 'location'
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'id': item_id, 'message': 'Location updated successfully'})
    }

def list_locations():
    response = table.query(
        KeyConditionExpression='record_type = :record_type_val',
        ExpressionAttributeValues={':record_type_val': 'location'}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Items', []))
    }

'''
Test Event: Create location
{
  "httpMethod": "POST",
  "path": "/locations",
  "body": "{\"name\":\"Visitor entrance\",\"vehicles_available\":\"3\"}"
}

Test Event: Create vehicle
{
  "httpMethod": "POST",
  "path": "/vehicles",
  "body": "{\"type\":\"Scooter\",\"available\":\"True\"}"
}

Test Event: Update location
{
  "httpMethod": "PUT",
  "path": "/locations",
  "body": "{\"id\":\"REPLACE_WITH_LOCATION_ID\",\"vehicles_available\":\"2\"}"
}

Test Event: Update vehicle
{
  "httpMethod": "PUT",
  "path": "/vehicles",
  "body": "{\"id\":\"REPLACE_WITH_VEHICLE_ID\",\"available\":\"False\"}"
}
'''