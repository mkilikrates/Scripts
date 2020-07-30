import logging
import traceback
import boto3
import json
import sys
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

