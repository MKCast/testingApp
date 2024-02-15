import json
import boto3
import bcrypt

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('RedTeamUserTable')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body.get('username')
    email = body.get('email')
    password = body.get('password')

    # Validate input data
    if not username or not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'All fields are required'})
        }

    # Hash the password securely
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Store user information in DynamoDB
    try:
        table.put_item(Item={
            'username': username,
            'email': email,
            'password': hashed_password
        })
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User registered successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
import boto3
import hashlib
import json

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('redteam_table')

def lambda_handler(event, context):
    # Extract email and password from the request body
    request_body = json.loads(event['body'])
    email = request_body.get('email')
    password = request_body.get('password')

    if not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Both email and password are required'})
        }

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Query DynamoDB to find the user by email
        response = user_table.get_item(Key={'email': email})
        user = response.get('Item')

        # Check if the user exists and if the hashed password matches
        if user and user['password'] == hashed_password:
            # Return authenticated status and user information
            return {
                'statusCode': 200,
                'body': json.dumps({'authenticated': True, 'user': user})
            }
        else:
            # Return authentication failure message
            return {
                'statusCode': 401,
                'body': json.dumps({'authenticated': False, 'message': 'Invalid email or password'})
            }
    except Exception as e:
        # Return error message if there's any issue with DynamoDB query
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }