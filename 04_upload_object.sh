#!/bin/bash

aws s3 sync ./image/ s3://ReplaceS3BucketName/
aws s3api put-bucket-policy \
  --bucket ReplaceS3BucketName \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ReplaceS3BucketName/*"
        }
    ]
}'
