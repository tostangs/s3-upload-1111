import base64
import os
import re
import gradio as gr
import boto3
import pprint
import botocore
import modules.scripts as scripts

from modules.ui_components import FormRow
from datetime import datetime
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
        
        with FormRow():
            with gr.Column():
                with FormRow():
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
        print('S3 Resource:')
        print(s3_resource)

        # Check if bucket exists and user has access...
        try:
            print("keys:")
            print(aws_access_key_id)
            print(aws_secret_access_key)
            res = s3_resource.meta.client.head_bucket(Bucket=bucket_name)
            print("Result check:")
            print(res)
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

        for i in range(len(processed.images)):
            print("\nThe preprocessed image object:")
            print(processed.images[i])

            regex = r"Steps:.*$"
            seed = processed.seed
            prompt = processed.prompt
            neg_prompt = processed.negative_prompt
            info = re.findall(regex, processed.info, re.M)[0]
            input_dict = dict(item.split(": ") for item in str(info).split(", "))
            steps = int(input_dict["Steps"])
            sampler = input_dict["Sampler"]
            cfg_scale = float(input_dict["CFG scale"])
            size = tuple(map(int, input_dict["Size"].split("x")))
            model_hash = input_dict["Model hash"]
            model = input_dict["Model"]

            # Set metadata for the file
            metadata = {
                'prompt': str(prompt),
                'negative-prompt': str(neg_prompt),
                'settings': str(steps),
                'type': 'GRAPHIC',
                'user_id': 'f6546399-112f-4ac4-bf1d-371e79c0a67f',
                'tags': '[]',
                'seed': str(seed),
                'org_id': 'G01H4KDWE9XB8T7HJT7QA4PQQHY',
                'model_hash': str(model_hash),
                'model': str(model),
                'size': str(size),
                'cfg_scale': str(cfg_scale),
                'sampler': str(sampler)
            }

            # Try to upload the processed image...
            try:
                curr_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
                img_data = BytesIO()
                processed.images[i].save(img_data, format='PNG')
                img_data.seek(0)
                s3_resource.Bucket(bucket_name).put_object(
                    Key=f'{collection_name}/auto1111_{i}_{curr_time}.png', 
                    Body=img_data,
                    Metadata=metadata
                )
                print(f'Image {i} uploaded successfully.')
                        
            except Exception as e:
                print(f"Something went wrong while uploading image {i}: {e}")
                continue
        return True

