import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
order_table = dynamodb.Table('redteam_orders')

def lambda_handler(event, context):
    try:
        # Extract order data from the API Gateway event
        body = json.loads(event['body'])
        user_id = body.get('user_id')
        order_items = body.get('order_items')
        total_cost = body.get('total_cost')

        # Store order information in DynamoDB
        response = order_table.put_item(
            Item={
                'user_id': user_id,
                'order_items': order_items,
                'total_cost': Decimal(total_cost)
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Order placed successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
