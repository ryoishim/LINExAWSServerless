import boto3

if __name__ == "__main__":

    BucketName='ryoishim-123456789'
	
    client=boto3.client('s3')

    #Create a bucket
    print('Creating bucket:' + BucketName)
    response=client.create_bucket(
        Bucket=BucketName,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-northeast-1'
        }
    )
    print('Status code: ' + str(response['ResponseMetadata']['HTTPStatusCode']))
    print('Created...')
