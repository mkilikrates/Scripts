#!/usr/bin/python3.8
import logging
import traceback
import boto3
import json
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)
hostname = ''
MPrivIP=''
MPubIP=''
MIPv6=''
PubIPV6={}
PrivIPV4={}
PubIPV4={}
hostedzones=''
instanceid = ''
region = ''
detailtype = ''
state = ''


