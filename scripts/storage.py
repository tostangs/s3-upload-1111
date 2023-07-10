import base64
import os
import re
import modules.scripts as scripts
import gradio as gr
import boto3
import pprint

from io import BytesIO
from modules.processing import process_images, Processed
from modules.processing import Processed

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
        bucket_name = gr.inputs.Textbox(label="Bucket Name", default="Enter Bucket Name")
        collection_name = gr.inputs.Textbox(label="Bucket Path", default="Enter Bucket path")
        return [checkbox_save_to_s3, bucket_name, collection_name]

    def postprocess(self, p, checkbox_save_to_s3, bucket_name, collection_name):
        pprint(p)
        print('in s3 upload postprocess method')
        if not checkbox_save_to_s3:
            return True
        print('after check to save to s3')

        # s3_resource = boto3_session.resource('s3')

        # Check if bucket exists
        # if s3_resource.Bucket(bucket_name) not in s3_resource.buckets.all():
        #     return True
        print('after check if user has access to the bucket')

        # for i in range(len(p.images)):
        #     print("\nThe preprocessed image object:")
            # pprint(p.images[i])
            # pprint(s3_resource)
            # pprint(p)
        print('after pretty printing objects')

        proc = process_images(p)

        return proc

