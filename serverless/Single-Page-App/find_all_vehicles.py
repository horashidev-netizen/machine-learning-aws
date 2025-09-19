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


def scan_table():
    try:
        result_item = []
        result_data = table.scan()

        result_item.extend(result_data['Items'])

        # Pagination https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.Pagination
        while 'LastEvaluatedKey' in result_data:
            result_data = table.scan(
                ExclusiveStartKey=result_data['LastEvaluatedKey']
            )
            result_item.extend(result_data['Items'])

        logger.info({"operation": "scan pets ", "details": result_item})

        return None, result_item
    except ClientError as err:
        logger.debug({"operation": "scan pets error ", "details": err})
        return err, None


def lambda_handler(event, context):
    logger.info(event)
    # Input Format https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    resource = event['resource']
    # Uncomment to print the event
    # print("Received event: " + json.dumps(event, indent=2))

    items = None
    err = None
    # /pets List all pets
    if (resource == "/vehicles"):
        err, items = scan_table()

    # /pets/petId find pet by Id
    else:
        err = 'This Lambda Function only work for Find All Pets, check for another Lambda Function'
        items = None

    response = response_payload(err, items)

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
