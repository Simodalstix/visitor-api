import boto3
import os
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'VisitorCounter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Increment the count
        user_agent = event['headers'].get('User-Agent', 'unknown')
        response = table.update_item(
            Key={'id': 'visitor_count'},
            UpdateExpression='ADD #c :inc',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

        # Get client IP (API Gateway v1 or v2 compatible)
        ip = event['headers'].get('X-Forwarded-For', 'unknown').split(',')[0]
        timestamp = datetime.utcnow().isoformat()

        # Create a new item to log this visitor
        table.put_item(
            Item={
                'id': f"ip:{ip}@{timestamp}",
                'ip': ip,
                'timestamp': timestamp,
                'user_agent': user_agent
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'visitor_count': int(response['Attributes']['count'])
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
