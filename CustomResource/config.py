import os
import sys
import json
import requests
import traceback
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
region = ''
accountId = ''
reqtype = ''
respurl = ''
stacktId = ''
requestId = ''
restype = ''
logresId = ''
resproper = ''

