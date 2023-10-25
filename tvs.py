# import boto3
# import os

# # Replace these with your S3 bucket name and preferred region
# s3_bucket_name = 'rcu-imagestore'
# # aws_region = 'us-east-1'  # Replace with your AWS region

# # Replace these with your access key ID and secret access key
# aws_access_key_id = 'AKIA3R25BEB7GE7KEB5P'
# aws_secret_access_key = 'xmJxazutfV16VEQAtiNkX5AyogTIw9b+xKobYxBd'

# # The local path to your Excel file
# local_file_path = 'red-x-icon.svg'

# # The key (object name) under which the file will be stored in S3
# s3_object_key = 'sample/red-x-icon.svg'

# # Create an S3 client using your credentials
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# # Upload the Excel file to the S3 bucket
# s3.upload_file(local_file_path, s3_bucket_name, s3_object_key)

# print(f"File '{local_file_path}' uploaded to S3 bucket '{s3_bucket_name}' as '{s3_object_key}'")

# import boto3

# # Replace these with your S3 bucket name, object key, and AWS credentials
# s3_bucket_name = 'rcu-imagestore'
# s3_object_key = 'sample/red-x-icon.svg'
# aws_access_key_id = 'AKIA3R25BEB7GE7KEB5P'
# aws_secret_access_key = 'xmJxazutfV16VEQAtiNkX5AyogTIw9b+xKobYxBd'

# # Create an S3 client using your AWS credentials
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# try:
#     # Use the head_object method to check if the object exists
#     s3.head_object(Bucket=s3_bucket_name, Key=s3_object_key)
#     print(f"S3 object '{s3_object_key}' exists in bucket '{s3_bucket_name}'")
# except s3.exceptions.ClientError as e:
#     if e.response['Error']['Code'] == '404':
#         print(f"S3 object '{s3_object_key}' does not exist in bucket '{s3_bucket_name}'")
#     else:
#         print(f"An error occurred: {e}")

import boto3

# Initialize an S3 client
s3 = boto3.client('s3')

# Specify the S3 bucket name and the object key
bucket_name = 'rcu-imagestore'
object_key = 'flamingo.jpeg'

# Generate a pre-signed URL for the object with a very large expiration time
url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': bucket_name,
        'Key': object_key
    },
    ExpiresIn=350000  # Set to an impractically large value
)

print("Object URL:", url)
