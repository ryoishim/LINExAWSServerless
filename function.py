import boto3
import json
import urllib
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Loading function")

rekognition_client = boto3.client("rekognition")
rek_threshold = 1
rek_max_faces = 1
rek_collection_id = "MyCollection"
channel_secret = os.environ["CHANNEL_ACCESS_TOKEN"]
LINE_BASE_URL = "https://api.line.me/v2/bot/message"
REPLY_URL = "https://ReplaceS3BucketName.s3-ap-northeast-1.amazonaws.com"


def get_image(message_id):
    """LINE Message APIサーバから、送信されたImageを取得"""

    url = f"{LINE_BASE_URL}/{message_id}/content"
    headers = {
        "Authorization": channel_secret,
        "Content-Type": "application/json"
    }
    request = urllib.request.Request(url, method="GET", headers=headers)
    with urllib.request.urlopen(request) as res:
        return res.read()


def get_face_match(body):
    """一致度判定"""

    response = rekognition_client.search_faces_by_image(
        CollectionId=rek_collection_id,
        Image={
            "Bytes": body,
        },
        FaceMatchThreshold=rek_threshold,
        MaxFaces=rek_max_faces
    )

    face_matches = response["FaceMatches"]
    logger.info("Matching faces")

    for match in face_matches:
        score = match["Similarity"]
        rek_message = f"一致度は{score:.2f}%でした！"
        rek_image_key = match["Face"]["ExternalImageId"]
        return {"rek_message": rek_message, "rek_image_key": rek_image_key}


def create_reply_request(reply_token, rek_message, image_url):
    """Reply用リクエスト生成"""

    url = f"{LINE_BASE_URL}/reply"
    method = "POST"
    headers = {
        "Authorization": channel_secret,
        "Content-Type": "application/json"
    }
    message = [
        {
            "type": "text",
            "text": "偉人との一致度を判定しました！\n判定結果は、、、、"
        },
        {
            "type": "image",
            "originalContentUrl": image_url,
            "previewImageUrl": image_url

        },
        {
            "type": "text",
            "text": str(rek_message)
        }
    ]
    params = {
        "replyToken": reply_token,
        "messages": message
    }
    return {"url": url, "header": headers, "body": message, "params": params, "method": method}


def lambda_handler(event, context):

    jsonstr = json.dumps(event, indent=2)
    logger.info("Received event: " + jsonstr)

    body = json.loads(event["Records"][0]["body"])
    timestamp = body["timestamp"]
    message_id = body["message"]["id"]
    reply_token = body["replyToken"]
    logger.info(f"timestamp: {timestamp}")
    logger.info(f"message_id: {message_id}")
    logger.info(f"reply_token: {reply_token}")

    # Messaging APIサーバから画像取得
    image_body = get_image(message_id)

    # 画像一致度取得
    rek_dict = get_face_match(image_body)
    logger.info(str(rek_dict))

    # Reply用画像URL生成
    image_key = rek_dict["rek_image_key"]
    image_url = f"{REPLY_URL}/{image_key}"
    logger.info(image_url)

    # Reply用リクエスト生成
    request_dict = create_reply_request(reply_token, rek_dict["rek_message"], image_url)
    logger.info(str(request_dict))

    request = urllib.request.Request(url=request_dict["url"], data=json.dumps(
        request_dict["params"]).encode("utf-8"),
        method=request_dict["method"], headers=request_dict["header"])

    with urllib.request.urlopen(request) as res:
        body = res.read()

    return 0
