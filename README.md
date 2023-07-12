
## Introduction

**s3-upload-11111** is an extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

This extension allows you to store pictures to your choice of AWS S3 bucket. At the moment it only supports AWS S3.

## Prerequisites

Before installing `s3-upload-11111`, you need to make sure that AWS CLI is installed and configured on your machine.

To install AWS CLI, follow the guide on the official AWS Documentation - [Installing AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

After successfully installing AWS CLI, you need to configure your access key ID and secret access key.

You can do this by running the following command in your terminal and providing your access key ID and secret access key when prompted:

```sh
aws configure
```

For more information, check out the guide [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

## Features

- **Store images into your chosen AWS S3 bucket instance**

## Installation

1. Ensure that AWS CLI is installed and properly configured with your Access Key ID and Secret Access Key.
2. Visit the **Extensions** tab within Automatic's WebUI.
3. Navigate to the **Install from URL** subtab.
4. Paste this repo's URL into the first field: `https://github.com/tostangs/s3-upload-1111`
5. Click **Install**.


## Usage
Set environment variables if needed before starting the application:
| Variable                 | Example                          |
|--------------------------|----------------------------------|
| `AWS_ACCESS_KEY_ID`      | `'<your_local_access_key_id>'`   |
| `AWS_SECRET_ACCESS_KEY`  | `<your_local_secret_access_key>` |

Then, simply check the `Save to S3` checkbox and generate!

## Contributing
I'm sure this plugin can be improved in many ways so feel free to submit PRs!
