import boto3
import json
import os
import logging
import base64
import hashlib
import hmac

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Loading function")

sqs_client = boto3.resource("sqs")
queue = sqs_client.get_queue_by_name(QueueName="LINEMessage")
channel_secret = os.environ["CHANNEL_SECRET"]


def is_image_type_message(message, timestamp):
    timestamp = timestamp
    m_id = message["id"]
    m_type = message["type"]
    logger.info(f"timestamp: {timestamp}")
    logger.info(f"message_id: {m_id}")
    if (m_type == "image"):
        logger.info("Send message to SQS because MessageType is image.")
        return True
    else:
        logger.info("MessageType is NOT image.")
        return False


def check_signature(event, x_line_signature):
    # SignatureVerification
    text = str(event)
    logger.info(f"Request-Body(event): {event}")
    logger.info(f"Request-Body(text): {text}")
    logger.info(f"event-type: {type(event)}")
    logger.info(f"text-type : {type(text)}")

    hash = hmac.new(channel_secret.encode("utf-8"),
                    text.encode("utf-8"), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    logger.info(f"Line-Signature: {x_line_signature}")
    logger.info(f"Body-Signature: {signature}")

    if x_line_signature.encode('utf-8') == signature:
        return True
    else:
        return False


def lambda_handler(event, context):

    jsonstr = json.dumps(event, indent=2)
    logger.info(f"Received event:: {jsonstr}")
    body_json = event["body"]
    events_json = json.loads(event["body"])
    
    x_line_signature = event["headers"]["X-Line-Signature"]

    # SignatureVerification
    check_result = check_signature(body_json, x_line_signature)
    logger.info(f"response : {check_result}")

    for e in events_json["events"]:
        if check_result == True and is_image_type_message(e["message"], e["timestamp"]):
            queue.send_message(MessageBody=json.dumps(e))

    body = {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "Empty Schema",
      "type": "object"
    }

    response = {
        'body': str(body),
        'statusCode': 200
    }

    return response
