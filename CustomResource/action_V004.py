import config
import ec2

def main():
    try:
        #locals
        name = config.resproper['CGWName']
        region = config.resproper['Region']
        asn = config.resproper['CGWASN']
        cert = config.resproper['CertificateArn']
        response = {}
        response['CustomerGateway'] = {}
        response['Reason'] = {}
        if config.reqtype == 'Create':
            action = ec2.create_customer_gateway(region,name,asn,cert)
            config.logger.info('Action: {}'.format(action))
            action["Reason"] = ("Custom Resource created!")
        elif config.reqtype == 'Delete':
            action = ec2.describe_customer_gateways(region,name,asn)
            config.logger.info('Action: {}'.format(action))
            cgwid = action['CustomerGateways']['CustomerGatewayId']
            action = ec2.delete_customer_gateway(region,cgwid)
            config.logger.info('Action: {}'.format(action))
            action["Reason"] = ("Custom Resource removed!")
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
            action["Reason"] = ("Nothing to do here!")
        response['CustomerGateway'] = action['CustomerGateway']
        response['Reason'] = action['Reason']
        action = {}
        action["statusCode"] = "200"
        action['Reason'] = {}
        action["Reason"] = response['Reason']
        action["CustomerGateway"] = {}
        action["CustomerGateway"] = response['CustomerGateway']
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
    return action