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
            action["PhysicalResourceId"] = action["CustomerGateways"]["CustomerGatewayId"]
        elif config.reqtype == 'Delete':
            cgwid = config.phyresId
            action = ec2.delete_customer_gateway(region,cgwid)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = 'None'
            action["Reason"] = ("Custom Resource removed!")
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
            action["Reason"] = ("Nothing to do here!")
        response['CustomerGateway'] = action['CustomerGateway']
        response['Reason'] = action['Reason']
        response['PhysicalResourceId'] = action['PhysicalResourceId']
        action = {}
        action["statusCode"] = "200"
        action['Reason'] = {}
        action["Reason"] = response['Reason']
        action["CustomerGateway"] = {}
        action["CustomerGateway"] = response['CustomerGateway']
        action['PhysicalResourceId'] = response['PhysicalResourceId']
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
    return action