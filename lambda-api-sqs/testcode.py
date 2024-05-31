import boto3
import random
import string
import json

def lambda_handler(event, context):
    # Create an SQS client
    sqs = boto3.client('sqs')

    # Get the queue URL
    queue_url = 'https://sqs.us-east-1.amazonaws.com/795337462110/test-queue'

    # Generate a random string of numbers
    random_numbers = ''.join(random.choices(string.digits, k=10))

    # Prepare the message body
    message_body = random_numbers

    # Send the message to the SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )

    print(f"Message sent to SQS queue: {message_body}")
    return {
        'statusCode': 200,
        'body': f"Message sent to SQS queue: {message_body}"
    }