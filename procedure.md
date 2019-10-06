# ハンズオン手順

## ■環境準備：Cloud9で新規環境を作成し、下記コマンドを実行する

```bash
git clone https://github.com/ryoishim/LINExAWSServerless.git
cd LINExAWSServerless
ls -l
sudo update-alternatives --config python ## python3.6を選択
sudo pip install boto3
```

## ■Rekognition環境構築

```bash
./00_init.sh
python 01_create_collection.py
python 02_describe_collection.py
python 03_create_bucket.py
./04_upload_object.sh
python 05_index_faces.py
```

### テストしてみよう

該当のS3バケットにinput.jpgという名前でファイルをアップロードし、下記のコマンドを実行してみてください。

```bash
python 06_search_faces_by_image.py
```

下記のような標準出力が得られると、正しく動作しています。  
下記の例だと、mig_53.jpgが最も似ている画像で、その精度は28.14%と推定されています。

```bash
$ python 06_search_faces_by_image.py
Matching faces
FileKey:mig_53.jpg
FaceId:34dd53ad-a30f-4a01-af63-933332c3402f
Similarity: 28.14%
```

## ■DynamoDBテーブル構築

## ■Lambda Function作成

## ■APIGateway作成

## ■LINE Messanging API設定
