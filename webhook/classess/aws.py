import boto3
from botocore.exceptions import ClientError
from datetime import datetime

import os

class AwsClient:

    aws_region = os.getenv('AWS_REGION')
    secret_manager_name = os.getenv('SECRET_MANAGER_NAME')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    cf_distribution_id = os.getenv('CF_DISTRIBUTION_ID')

    def __init__(self):
        pass

    def invalidate_cache(self, url):
        self.url = url
        self.get_call_ref = datetime.now().strftime("%H%M%s")
        print("url", self.url, self.get_call_ref)

        cf_client = boto3.client(
            'cloudfront',
            aws_access_key_id = AwsClient.aws_access_key,
            aws_secret_access_key = AwsClient.aws_secret_key
        )

        create_invalidation = cf_client.create_invalidation(
            DistributionId = AwsClient.cf_distribution_id,
            InvalidationBatch = {
                'Paths' : {
                    'Quantity' : 1,
                    'Items' : [
                        self.url
                    ]
                },
                'CallerReference': self.get_call_ref
            }
        )
        
        

    def get_secret_manager(self):
        session = boto3.session.Session()
        client = session.client(
            service_name = 'secretsmanager',
            region_name = AwsClient.aws_region
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=AwsClient.secret_manager_name
            )
        except ClientError as err:
            raise err
        
        secret_key = get_secret_value_response['SECRET_KEY']
        access_key = get_secret_value_response['ACCESS_KEY']

