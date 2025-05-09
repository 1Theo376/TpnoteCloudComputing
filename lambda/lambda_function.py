import json
import os
import boto3

sqs = boto3.client('sqs') #client is required to interact with sqs
OUTPUT_QUEUE_URL = os.getenv("OUTPUT_QUEUE_URL")  # URL de la file SQS de sortie

def lambda_handler(event, context):
    results = []

    for record in event['Records']:
        message = json.loads(record['body'])
        number1 = float(message['number1'])
        number2 = float(message['number2'])
        operation = message['operation']

        if operation == "+":
            result = number1 + number2
        elif operation == "-":
            result = number1 - number2
        elif operation == "*":
            result = number1 * number2
        elif operation == "/":
            if number2 == 0:
                result = "La division par zéro est impossible"
            else:
                result = number1 / number2
        else:
            result = "Opération inconnue"

        sqs.send_message(
                QueueUrl=OUTPUT_QUEUE_URL,
                MessageBody=json.dumps({"result": result})
            )

        results.append(result)

    return {
        'statusCode': 200,
        'body': json.dumps(results)
        }
