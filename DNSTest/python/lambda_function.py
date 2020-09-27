import json
import dns
import logging
import traceback
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    config.logger.info('event: {}'.format(event))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

