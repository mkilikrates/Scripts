import sys
import json
import traceback
import logging
import boto3
from netaddr import *
logger = logging.getLogger()
logger.setLevel(logging.INFO)
region = ''
accountId = ''
requestId = ''
transformId = ''
fragment = {}
params = {}
templateParameterValues = {}
templateaction = ''

