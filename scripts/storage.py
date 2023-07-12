import base64
import os
import re
import modules.scripts as scripts
import gradio as gr
import boto3
import pprint
import botocore

from io import BytesIO
from modules.processing import process_images, Processed


aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')

boto3_session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

s3_client = boto3_session.client('s3')

class Scripts(scripts.Script):
    def title(self):
        return "S3 Uploader"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        checkbox_save_to_s3 = gr.inputs.Checkbox(label="Save to s3", default=False)
        bucket_name = gr.inputs.Textbox(label="Bucket Name", placeholder="Enter Bucket Name")
        collection_name = gr.inputs.Textbox(label="Bucket Path", placeholder="Enter Bucket path")
        return [checkbox_save_to_s3, bucket_name, collection_name]

    def postprocess(self, p, processed, checkbox_save_to_s3, bucket_name, collection_name):
        print('in s3 upload postprocess method')
        if not checkbox_save_to_s3:
            return True
        print('after check to save to s3')

        s3_resource = boto3_session.resource('s3')

        # Check if bucket exists and user has access...
        try:
            print("keys:")
            print(aws_access_key_id)
            print(aws_secret_access_key)
            s3_resource.meta.client.head_bucket(Bucket=bucket_name)
            print('S3 Resource:')
            print(s3_resource)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                print("Private Bucket. Forbidden Access!")
                print(e.response)
                return False
            elif error_code == 404:
                print("Bucket Does Not Exist!")
                print(e.response)
                return False

        print('after check if user has access to the bucket')

        for i in range(len(p.images)):
            print("\nThe preprocessed image object:")
            pprint(p.images[i])
            pprint(s3_resource)

            # Try to upload the processed image...
            try:  
                img_data = BytesIO()
                p.images[i].save(img_data, format='PNG')
                img_data.seek(0)
                s3_resource.Bucket(bucket_name).put_object(Key=f'{collection_name}/image_{i}.png', Body=img_data)
                print(f'Image {i} uploaded successfully.')
                
            except Exception as e:
                print(f"Something went wrong while uploading image {i}: {e}")
                continue 
        return True

