import boto3, json
import urllib
import re
import os
import logging
import base64
import hashlib
import hmac

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from datetime import datetime

logger.info('Loading function')

## def Const var
sqsClient = boto3.resource("sqs")
queue = sqsClient.get_queue_by_name(QueueName='LINEMessage')
channelSecret = os.environ['CHANNEL_ACCESS_TOKEN']

def lambda_handler(event, context):

    jsonstr = json.dumps(event, indent=2)
    logger.info("Received event: " + jsonstr)


    # SignatureVerification
    hash = hmac.new(channelSecret.encode('utf-8'),
        str(event['body-json']['events'][0]).encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    logger.info("Line-Signature: " + event['params']['header']['X-Line-Signature'])
    logger.info("Body-Signature: " + str(signature))

    for e in event['body-json']['events']:
    # e が画像のメッセージかどうか判別
        timestamp = e['timestamp']
        messageId = e['message']['id']
        logger.info("timestamp: " + str(timestamp))
        logger.info("messageId: " + str(messageId))
        if (e['message']['type'] == "image"):
            logger.info("Send message to SQS because MessageType is image.")
            queue.send_message(MessageBody=json.dumps(e))
        else:
            logger.info("MessageType is NOT image.")

    return 0    
