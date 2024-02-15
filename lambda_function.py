from awslambdaric import lambda_handler
import app  # Import your Flask app

def handler(event, context):
    return lambda_handler(app.app, event, context)
