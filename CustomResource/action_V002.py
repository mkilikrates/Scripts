import config
import ec2

def main():
    try:
        #locals
        region = config.resproper['Region']
        domain = config.resproper['Domain']
        if config.reqtype == 'Create':
            action = ec2.allocate_address(region,domain)
            config.logger.info('Action: {}'.format(action))
        elif config.reqtype == 'Delete':
            addr = []
            addr.append(config.resproper['PublicIp'])
            action = ec2.describe_addresses(region,addr)
            config.logger.info('Action: {}'.format(action))
            addraloc = action['Addresses']['AllocationId']
            action = ec2.release_address(region,addraloc)
            config.logger.info('Action: {}'.format(action))
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
        response = {}
        response['Addresses'] = {}
        response['Addresses'] = action
        action = {}
        action["statusCode"] = "200"
        action["Reason"] = ("Custom Resource found!")
        action["Addresses"] = {}
        action["Addresses"] = response['Addresses']
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
    return action