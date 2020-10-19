#!/usr/bin/python3
import os
import sys
import argparse
import logging
import traceback
import boto3
import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)
lamdamaps3bucket = 'mauranjo'
lamdamaps3key = 'lambda/Mappings/zonemap.cfg'

parser = argparse.ArgumentParser(description='Update lambdas', prog='updatecfn.py', usage='%(prog)s [options]')
parser.add_argument('-r', '--region', action='store', type=str, help='aws region like eu-west-1', default='eu-west-1', dest='region')
parser.add_argument('-c', '--cfnname', action='store',type=str, help='cfn template or all', default='all', dest='cfnname')
args = parser.parse_args()
region = args.region
cfnname = args.cfnname
print ("Region is " + region)
print ("CFN is " + cfnname)

s3_obj = boto3.client('s3')
response = s3_obj.get_object(Bucket=lamdamaps3bucket, Key=lamdamaps3key)
zonemap = json.loads((response['Body']).read())
print (zonemap)



