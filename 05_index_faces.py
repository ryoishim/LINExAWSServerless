#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

if __name__ == "__main__":

    bucket='ReplaceS3BucketName'
    collectionId='MyCollection'

    client=boto3.client('rekognition')
    s3client=boto3.client('s3')
    response = s3client.list_objects(
        Bucket=bucket,
        Prefix='img'
    )

    if 'Contents' in response:
        keys = [content['Key'] for content in response['Contents']]

    for photo in keys:
       response=client.index_faces(CollectionId=collectionId,
                                   Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                   ExternalImageId=photo,
                                   MaxFaces=1,
                                   QualityFilter="AUTO",
                                   DetectionAttributes=['ALL'])

       print ('Results for ' + photo) 	
       print('Faces indexed:')						
       for faceRecord in response['FaceRecords']:
            print('  Face ID: ' + faceRecord['Face']['FaceId'])
            print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

       print('Faces not indexed:')
       for unindexedFace in response['UnindexedFaces']:
           print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
           print(' Reasons:')
           for reason in unindexedFace['Reasons']:
               print('   ' + reason)
