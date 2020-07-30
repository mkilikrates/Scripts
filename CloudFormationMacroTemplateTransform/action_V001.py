import config
import stack

def main():
    try:
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        UpdateDNS = config.templateParameterValues['UpdateDNS']
        PrivHZ = config.templateParameterValues['PRIVHOSTEDZONEID']
        vpcname = config.templateParameterValues['VpcName']
        DualStack = config.templateParameterValues['DualStack']
        VpcCidr = config.templateParameterValues['VpcCidr']
        PubSub = config.templateParameterValues['PubSub']
        PubSize = int(config.templateParameterValues['PubSize'])
        PubSubAZs = config.templateParameterValues['PubSubAZs']
        PrivSub = config.templateParameterValues['PrivSub']
        PrivSize = int(config.templateParameterValues['PrivSize'])
        PrivSubAZs = config.templateParameterValues['PrivSubAZs']
        NatGW = config.templateParameterValues['NatGW']
        action = stack.vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW)
        config.logger.info('Response: {}'.format(action))
        action = {}
        action["statusCode"] = "200"
        action["body"] = config.json.dumps('Template Update Success!')
        config.logger.info('Response: {}'.format(action))
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["body"] = str(e)
        config.logger.info('Response: {}'.format(action))
    return action
