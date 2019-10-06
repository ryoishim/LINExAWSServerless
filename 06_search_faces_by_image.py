#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

if __name__ == "__main__":

    bucket='ReplaceS3BucketName'
    collectionId='MyCollection'
    fileName='input.jpg'
    threshold = 1
    maxFaces = 1

    client=boto3.client('rekognition')

  
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print 'Matching faces'
    for match in faceMatches:
            print 'FileKey:' + match['Face']['ExternalImageId']
            print 'FaceId:' + match['Face']['FaceId']
            print 'Similarity: ' + "{:.2f}".format(match['Similarity']) + "%"
            print

