import config
import action_V001
import action_V002
def handler(event, context):
    config.logger.info('event: {}'.format(event))
    config.logger.info('context: {}'.format(context))
    response = {
        "Status": "SUCCESS",
        "RequestId": event['RequestId'],
        "StackId": event['StackId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "PhysicalResourceId" : "None",
        "Reason": "Nothing to do",
        "Data": {}
    }
    try:
        # Globals
        config.region = config.os.environ['AWS_REGION']
        config.reqtype = event['RequestType']
        config.stacktId = event['StackId']
        config.requestId = event['RequestId']
        config.restype = event['ResourceType']
        config.logresId = event['LogicalResourceId']
        config.resproper = event['ResourceProperties']
        config.respurl = event['ResponseURL']
        if config.resproper['Version'] == 'V0.0.1':
            try:
                action = action_V001.main()
                config.logger.info('Response: {}'.format(action))
                response["Reason"] = action["Reason"]
                response["Data"]["DnsIpAddrs"] = []
                response["Data"]["DnsIpAddrs"] = action["DnsIpAddrs"]
            except Exception as e:
                config.logger.error('ERROR: {}'.format(e))
                config.traceback.print_exc()
                response["Reason"] = str(e)
                response["Status"] = "FAILED"
        if config.resproper['Version'] == 'V0.0.2':
            try:
                action = action_V002.main()
                config.logger.info('Response: {}'.format(action))
                response["Reason"] = action["Reason"]
                response["Data"] = action["Addresses"]
            except Exception as e:
                config.logger.error('ERROR: {}'.format(e))
                config.traceback.print_exc()
                response["Reason"] = str(e)
                response["Status"] = "FAILED"
        if not 'statusCode' in action:
            response["Reason"] = config.json.dumps('Nothing to do with requestId: ' + config.requestId)
    except Exception as e:
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["Reason"] = str(e)
        response["Status"] = "FAILED"
    config.logger.info('Sending Response')
    config.logger.info('response: {}'.format(response))
    response_data = config.json.dumps(response)
    headers = {
        'content-type': '',
        'content-length': str(len(response_data))
    }
    try:
        action = config.requests.put(config.respurl,data=response_data,headers=headers)
        config.logger.info('CloudFormation returned status code: {}'.format(response["Reason"]))
    except Exception as e:
        config.logger.info('send(..) failed executing requests.put(..): {}'.format(e))
        raise
    return response

