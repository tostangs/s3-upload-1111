import base64
from io import BytesIO
import os
import simplejson as json
import re
import modules.scripts as scripts
import gradio as gr
import boto3

aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')

boto3_session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def get_collection(bucket_name, collection_name):
    bucket = boto3_session[bucket_name]
    collection = bucket[collection_name]
    return collection

class Scripts(scripts.Script):
    def title(self):
        return "S3 Uploader"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        checkbox_save_to_s3 = gr.inputs.Checkbox(label="Save to s3", default=False)
        bucket_name = gr.inputs.Textbox(label="Bucket Name", default="StableDiffusion")
        collection_name = gr.inputs.Textbox(label="Collection Name", default="Automatic1111")
        return [checkbox_save_to_s3, bucket_name, collection_name]

    def postprocess(self, p, processed,checkbox_save_to_s3,bucket_name,collection_name):
        collection = get_collection(bucket_name, collection_name) if checkbox_save_to_s3 else None
        if collection is None:
            return True
        
        for i in range(len(processed.images)):

            json_str = json.dumps(processed.images[i], indent=4, sort_keys=True)
            print("\nThe preprocessed image object:")
            print(json_str)
        return True
