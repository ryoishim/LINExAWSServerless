import boto3, json
import urllib
import re
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from datetime import datetime

logger.info('Loading function')      # Functionのロードをログに出力


# 定数を定義
dynamoDBClient = boto3.resource("dynamodb")
rekognitionClient = boto3.client('rekognition')
rekThreshold = 1
rekMaxFaces = 1
rekCollectionId = 'MyCollection'

def lambda_handler(event, context):
    # 文字列へ変換
    jsonstr = json.dumps(event, indent=2)
    logger.info("Received event: " + jsonstr)

    timestamp = event['events'][0]['timestamp']
    messageId = event['events'][0]['message']['id']
    logger.info("timestamp: " + str(timestamp))
    logger.info("messageId: " + str(messageId))

    # LINE Message APIサーバから、送信されたImageを取得
    url = "https://api.line.me/v2/bot/message/"+str(messageId)+"/content"
    method = "GET"
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    request = urllib.request.Request(url, method=method, headers=headers)
    with urllib.request.urlopen(request) as res:
        body = res.read()
    
    # 一致度判定
    response=rekognitionClient.search_faces_by_image(
        CollectionId=rekCollectionId,
        Image={
            'Bytes': body,
        },
        FaceMatchThreshold=rekThreshold,
        MaxFaces=rekMaxFaces
    )
                                
    faceMatches=response['FaceMatches']
    logger.info('Matching faces')
    rek_message = ''

    for match in faceMatches:
        rek_message += '一致度は' + "{:.2f}".format(match['Similarity']) + '%でした！'

    logger.info(rek_message)
    
    # Reply用画像URL生成
    KEY = match['Face']['ExternalImageId']
    image_url='https://ReplaceS3BucketName.s3-ap-northeast-1.amazonaws.com/' + KEY
    logger.info(image_url)
    
    # Reply用リクエスト生成
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    message = [
      {
        'type': 'text',
        'text': '偉人との一致度を判定しました！\n判定結果は、、、、'
      },
      {
        'type': 'image',
        'originalContentUrl': image_url,
        'previewImageUrl': image_url
        
      },
      {
        'type': 'text',
        'text': str(rek_message)
      }
    ]
    params = {
        "replyToken": event['events'][0]['replyToken'],
        "messages": message
    }
    request = urllib.request.Request(url, json.dumps(params).encode("utf-8"), method=method, headers=headers)
    with urllib.request.urlopen(request) as res:
        body = res.read()
    return 0    
