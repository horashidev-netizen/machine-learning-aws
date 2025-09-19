import boto3
from botocore.exceptions import ClientError
import logging
import json

# AWS Lambda Function Logging in Python - https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
logger = logging.getLogger()
logger.setLevel(logging.INFO)


session = boto3.Session()
dynamodb = session.resource("dynamodb")

table_name = "vehicles"

table = dynamodb.Table(table_name)


def query_item(id):
    try:
        ret = table.get_item(
         Key={'id': id}
        )
        logger.info({"operation": "query a pet ", "details": ret})
        # Return the Item - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item
        return None, ret['Item']
        
    except ClientError as err:
         logger.debug({"operation": "query a pet error ", "details": err})
         return err, None
        

def lambda_handler(event, context):
    logger.info(event)
    # Input Format https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    resource = event['resource']
    # Uncomment to print the event
    # print("Received event: " + json.dumps(event, indent=2))

    item = None
    err = None

    # /pets/petId find pet by Id
    if (resource == "/vehicles/{id}"):
        petId = event['pathParameters']['id']
        err, item = query_item(petId)
    else:
        err = 'This Lambda Function only work for Find Pet Detail, check for another Lambda Function'
        item = None


    response = response_payload(err, item)

    return response


'''
In Lambda proxy integration, API Gateway sends the entire request as input to a backend Lambda function. 
API Gateway then transforms the Lambda function output to a frontend HTTP response.
Output Format: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format
'''


def response_payload(err, res=None):
    if err:
        error_message = str(err)
        status_code = "502"
        response_body = {"error": {"message": error_message}}
    else:
        status_code = "200"
        response_body = res

    return {
        "statusCode": status_code,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
    }