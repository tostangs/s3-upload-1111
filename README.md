## Introduction

**s3-upload-11111 is an extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).**

It allows to store pictures to your choice of aws s3 bucket. At the moment it only supports aws s3.
## Features

- **Store images into your s3 bucket instance**

## Installation


1. Visit the **Extensions** tab of Automatic's WebUI.
2. Visit the **Install from URL** subtab.
3. Paste this repo's URL into the first field: `https://github.com/tostangs/s3-upload-1111`
4. Click **Install**.

## Usage
Set environment variables if needed before starting the app:
| Variable                 | Example                          |
|--------------------------|----------------------------------|
| `AWS_ACCESS_KEY_ID`      | `'<your_local_access_key_id>'`   |
| `AWS_SECRET_ACCESS_KEY`  | `<your_local_secret_access_key>` |

Then, simply check the `Save to S3` checkbox and generate!


## Contributing
I'm sure this plugin can be improved in many ways so feel free to submit PRs!
