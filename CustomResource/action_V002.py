import config
import ec2

def main():
    try:
        #locals
        region = config.resproper['AllocateAddress']['Region']
        domain = config.resproper['AllocateAddress']['Domain']
        response = {}
        response['Addresses'] = {}
        if config.reqtype == 'Create':
            action = ec2.allocate_address(region,domain)
            config.logger.info('Action: {}'.format(action))
            response["PhysicalResourceId"] = action['AllocationId']
        elif config.reqtype == 'Delete':
            addraloc = config.phyresId
            action = ec2.release_address(region,addraloc)
            config.logger.info('Action: {}'.format(action))
            response["PhysicalResourceId"] = 'None'
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
        response['Addresses'] = action
        response["Reason"] = action["Reason"]
        response["statusCode"] = action["statusCode"]
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response