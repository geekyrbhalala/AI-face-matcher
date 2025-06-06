import boto3
from config import S3_BUCKET, AWS_REGION
from pathlib import Path

def upload_to_s3(file_path, bucket, key):
    try:
        s3 = boto3.client('s3', region_name = AWS_REGION)
        s3.upload_file(file_path,bucket,key)
        print(f"✅ Uploaded {file_path} to s3://{bucket}/{key}")
    except Exception as e:
        print(f"❌ Error uploading {file_path} to s3://{bucket}/{key}: {e}")

def compare_faces(bucket,source_key,target_key):
    rekognition = boto3.client('rekognition', region_name=AWS_REGION)

    response = rekognition.compare_faces(
        SourceImage={'S3Object':{'Bucket': bucket, 'Name': source_key}},
        TargetImage={'S3Object':{'Bucket': bucket, 'Name': target_key}},
        SimilarityThreshold=80
    )

    matches = response['FaceMatches']

    if matches:
        similarity = matches[0]['Similarity']
        print(f"🎯 Face match found! Similarity: {similarity:.2f}%")
    else:
        print("❌ No matching faces found.")


#Main logic

if __name__ == "__main__":
    source_img = "images/id_photo.jpg"
    target_img = "images/selfie.jpg"

    #Upload images to S3
    upload_to_s3(source_img, S3_BUCKET, Path(source_img).name)
    upload_to_s3(target_img, S3_BUCKET, Path(target_img).name)

    #Compare faces
    compare_faces(S3_BUCKET, Path(source_img).name, Path(target_img).name)