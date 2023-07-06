import launch

if not launch.is_installed("s3upload"):
    launch.run_pip("install s3uplaod", "requirements for s3-upload-1111")