#!/bin/bash

echo -n "ユニークとなるバケット名を入力して下さい(ex: 20191106-ryoishim-handson):"
read input
sed -e "s/ReplaceS3BucketName/${input}/" ./03_create_bucket.py
#sed -e "s/ReplaceS3BucketName/${input}/" ./04_upload_object.sh
#sed -e "s/ReplaceS3BucketName/${input}/" ./05_index_faces.py
#sed -e "s/ReplaceS3BucketName/${input}/" ./06_search_faces_by_image.py
#sed -e "s/ReplaceS3BucketName/${input}/" ./function.py
