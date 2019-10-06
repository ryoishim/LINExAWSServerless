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

投稿された画像と、偉人の一致度を判定するための環境を構築します。  
今回は事前に登録されたデータセットとの一致度を判定する、 `Collection` 機能を利用します。  
https://docs.aws.amazon.com/ja_jp/rekognition/latest/dg/collections.html  
作成用のスクリプトを準備済みですので、下記の通り実行してみてください。  
また、余裕があれば各スクリプト内でどのような処理を実施しているか確認してみてください。

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

## ■ 4. Lambda Function作成

### 4-1. Lambda用IAMロール作成

LambdaからDynamoDBにアイテムをPutしたり、Rekognitionを呼び出したりする、また様々な機能を組み合わせる上で認可の仕組みが必要となります。  
AWSでは、IAMロールを使って実現することができます。  
今回は、Lambda Functionを作成する前に必要なIAMロールを作成します。

<img src="./pr_image/lambda_1.png" width=50%><br>
↓  
<img src="./pr_image/lambda_2.png" width=50%><br>
↓  
<img src="./pr_image/lambda_3.png" width=50%><br>
↓  
<img src="./pr_image/lambda_4.png" width=50%><br>
↓  
<img src="./pr_image/lambda_5.png" width=50%><br>

### 4-2. Lambda Function作成

さて、Lambda Function用のIAMロールが作成できたので、実際にLambda Functionを作成します。  
サンプルコードを、cloneされたリポジトリ内に格納されている `function.py` としてご提供しております。  
下記手順のとおり、 `Python3.6` 環境でLambda Functionを作成し、GUIウィンドウより該当のコードをLambdaに設定してください。

<img src="./pr_image/lambda_6.png" width=50%><br>
↓  
<img src="./pr_image/lambda_7.png" width=50%><br>
↓  
<img src="./pr_image/lambda_8.png" width=50%><br>
↓  
<img src="./pr_image/lambda_9.png" width=50%><br>

本来であれば、この時点でLambdaに対してSample Eventを与えてテストを実行しますが、本コードではLINEのAuthentication Tokenが必要となるため先に進みます。

## ■ 5. APIGateway作成

LINE Messaging APIからのリクエストをhttpsで受け付け、LambdaにプロキシするためのGatewayが必要となります。  
今回は、シンプルなPUTメソッドをもつAPIgatewayを作成します。

## ■ 6. LINE Messanging API設定

さて、ここまでくるとLINEとの統合を設定することができます。  
下記サイトにアクセスして、右上の `ログイン` ボタンより、ご自身のLINE IDを使ってアカウント作成/ログインしてみましょう。
https://developers.line.biz/ja/

## ■ (optional) 7. RekognitionのAPIを使ってより拡張してみよう

今回は事前に用意されたデータセットに対する偉人判定を実施しましたが、  
Rekognitionには他にも様々な機能が搭載されています。  
例えば、以下のようなことを簡単に実現することができます。

* 人物の表情判定をする方法は？
* 写真に写っている人数を数える方法は？
* 人物を有名人であるか判定する方法は？

LINEとAWSが提供するソリューションをうまく組み合わせて、さらなる拡張を考えてみましょう。  
**「可能性はアイデア次第で無限大です！」**
