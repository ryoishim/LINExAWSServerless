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
channel_secret = os.environ["CHANNEL_ACCESS_TOKEN"]


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


def check_signature(event):
    # SignatureVerification
    text = str(event["body-json"])
    x_line_signature = event["params"]["header"]["X-Line-Signature"]
    hash = hmac.new(channel_secret.encode("utf-8"),
                    text.encode("utf-8"), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    logger.info(f"Line-Signature: {x_line_signature}")
    logger.info(f"Body-Signature: {signature}")


def lambda_handler(event, context):

    jsonstr = json.dumps(event, indent=2)
    logger.info(f"Received event:: {jsonstr}")

    # SignatureVerification
    check_signature(event)

    for e in event["body-json"]["events"]:
        if is_image_type_message(e["message"], e["timestamp"]):
            queue.send_message(MessageBody=json.dumps(e))

    return 0
