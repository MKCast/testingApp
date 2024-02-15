import json
import boto3

dynamodb = boto3.resource('dynamodb')
menu_table = dynamodb.Table('redteam_menu')

def lambda_handler(event, context):
    try:
        # Fetch menu items from DynamoDB
        response = menu_table.scan()
        menu_items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps({'menu_items': menu_items})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
