def preload(parser):
    parser.add_argument("--s3-bucketname", type=str, help="S3 Bucketname", default="none")
    parser.add_argument("--s3-bucketpath", type=str, help="S3 Bucketpath", default="none")