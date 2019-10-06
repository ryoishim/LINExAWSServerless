import boto3, json
import urllib
import re
import os

from datetime import datetime

print('Loading function')      # Functionのロードをログに出力

def lambda_handler(event, context):
    # 文字列へ変換
    jsonstr = json.dumps(event, indent=2)
    print("Received event: " + jsonstr)

    timestamp = event['events'][0]['timestamp']
    messageId = event['events'][0]['message']['id']
    print("timestamp: " + str(timestamp))
    print("messageId: " + str(messageId))

    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table("LINETable") # DynamoDBのテーブル名

    # DynamoDBへのPut処理実行
    table.put_item(
      Item = {
        "timestamp": str(timestamp),
        "message": jsonstr
      }
    )

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
    client = boto3.client('rekognition')
    collectionId='MyCollection'
    threshold = 1
    maxFaces = 1
    response=client.search_faces_by_image(
        CollectionId=collectionId,
        Image={
            'Bytes': body,
        },
        FaceMatchThreshold=threshold,
        MaxFaces=maxFaces
    )
                                
    faceMatches=response['FaceMatches']
    print('Matching faces')
    rek_message = ''

    for match in faceMatches:
        rek_message += '一致度は' + "{:.2f}".format(match['Similarity']) + '%でした！'

    print(rek_message)
    
    # Reply用画像URL生成
    KEY = match['Face']['ExternalImageId']
    image_url='https://ReplaceS3BucketName.s3-ap-northeast-1.amazonaws.com/' + KEY
    print(image_url)
    
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
