import boto3

client = boto3.client('sqs')

response = client.create_queue(
    QueueName='test-queue'
)
print(response['QueueUrl'])
