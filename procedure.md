# ハンズオン手順

## ■ 1. 環境準備：Cloud9で新規環境を作成し、下記コマンドを実行する

### 1-1. デフォルト設定でCloud9の環境を作成する

<img src="./pr_image/cloud9_1.png" width=50%><br>
↓  
<img src="./pr_image/cloud9_2.png" width=50%><br>
↓  
<img src="./pr_image/cloud9_3.png" width=50%><br>
↓  
<img src="./pr_image/cloud9_4.png" width=50%><br>
↓  
<img src="./pr_image/cloud9_5.png" width=50%><br>
↓  
<img src="./pr_image/cloud9_6.png" width=50%><br>

### 1-2. 下記の初期化手順を実施する

```bash
git clone https://github.com/ryoishim/LINExAWSServerless.git
cd LINExAWSServerless
ls -l
sudo update-alternatives --config python ## python3.6を選択
sudo pip install boto3
```

## ■ 2. Rekognition環境構築

### 2-1. コレクション/S3バケット作成/オブジェクトアップロード

```bash
./00_init.sh
python 01_create_collection.py
python 02_describe_collection.py
python 03_create_bucket.py
./04_upload_object.sh
python 05_index_faces.py
```
### 2-2. (optional)テストしてみよう

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
## ■ 3. DynamoDBテーブル構築

LINE Messaging APIから送信されるPayloadを保管するDynamoDBテーブルを作成します。

### 3-1. DynamoDBテーブル構築(LINE Table)

<img src="./pr_image/ddb_1.png" width=50%><br>
↓  
<img src="./pr_image/ddb_2.png" width=50%><br>
↓  
<img src="./pr_image/ddb_3.png" width=50%><br>

DynamoDBはテーブル名の大文字小文字を判定する仕様(CaseSensitive)であることにご注意ください

## ■Lambda Function作成

## ■APIGateway作成

## ■LINE Messanging API設定
