import config
import action_V001
import action_V002
import action_V003
def handler(event, context):
    config.logger.info('event: {}'.format(event))
    response = {
        "requestId": event['requestId'],
        "status": "success",
        "fragment": event["fragment"]
    }
    try:
        # Globals
        config.region = event['region']
        config.accountId = event['accountId']
        config.fragment = event['fragment']
        config.transformId = event['transformId']
        config.params = event['params']
        config.requestId = event['requestId']
        config.templateParameterValues = event['templateParameterValues']
        # Retrieve Parameters passing to the CF
        config.templateaction = config.fragment['Description']
        if config.templateaction == 'V0.0.1':
            try:
                action = action_V001.main()
                config.logger.info('Response: {}'.format(action))
                response["statusCode"] = action["statusCode"]
                response["body"] = action["body"]
            except Exception as e:
                config.logger.error('ERROR: {}'.format(e))
                config.traceback.print_exc()
                response["statusCode"] = "500"
                response["body"] = str(e)
        if config.templateaction == 'V0.0.2':
            try:
                action = action_V002.main()
                config.logger.info('Response: {}'.format(action))
                response["statusCode"] = action["statusCode"]
                response["body"] = action["body"]
            except Exception as e:
                config.logger.error('ERROR: {}'.format(e))
                config.traceback.print_exc()
                response["statusCode"] = "500"
                response["body"] = str(e)
        if config.templateaction == 'V0.0.3':
            try:
                action = action_V003.main()
                config.logger.info('Response: {}'.format(action))
                response["statusCode"] = action["statusCode"]
                response["body"] = action["body"]
            except Exception as e:
                config.logger.error('ERROR: {}'.format(e))
                config.traceback.print_exc()
                response["statusCode"] = "500"
                response["body"] = str(e)
        if not 'statusCode' in response:
            response["statusCode"] = "200"
            response["body"] = config.json.dumps('Nothing to do with requestId: ' + config.requestId)
        config.logger.info (response)
        config.logger.info('event: {}'.format(event))
        return response
    except Exception as e:
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response


