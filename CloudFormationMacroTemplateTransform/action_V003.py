import config
import stack

def main():
    try:
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        UpdateDNS = 'No'
        PrivHZ = ''
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

        vpcname = config.templateParameterValues['VpcName1']
        DualStack = config.templateParameterValues['DualStack1']
        VpcCidr = config.templateParameterValues['VpcCidr1']
        PubSub = config.templateParameterValues['PubSub1']
        PubSize = int(config.templateParameterValues['PubSize1'])
        PubSubAZs = config.templateParameterValues['PubSubAZs1']
        PrivSub = config.templateParameterValues['PrivSub1']
        PrivSize = int(config.templateParameterValues['PrivSize1'])
        PrivSubAZs = config.templateParameterValues['PrivSubAZs1']
        NatGW = config.templateParameterValues['NatGW1']
        action = stack.vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW)
        config.logger.info('Response: {}'.format(action))

        vpcname = config.templateParameterValues['VpcName2']
        DualStack = config.templateParameterValues['DualStack2']
        VpcCidr = config.templateParameterValues['VpcCidr2']
        PubSub = config.templateParameterValues['PubSub2']
        PubSize = int(config.templateParameterValues['PubSize2'])
        PubSubAZs = config.templateParameterValues['PubSubAZs2']
        PrivSub = config.templateParameterValues['PrivSub2']
        PrivSize = int(config.templateParameterValues['PrivSize2'])
        PrivSubAZs = config.templateParameterValues['PrivSubAZs2']
        NatGW = config.templateParameterValues['NatGW2']
        action = stack.vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW)
        config.logger.info('Response: {}'.format(action))

        vpcname = config.templateParameterValues['VpcName3']
        DualStack = config.templateParameterValues['DualStack3']
        VpcCidr = config.templateParameterValues['VpcCidr3']
        PubSub = config.templateParameterValues['PubSub3']
        PubSize = int(config.templateParameterValues['PubSize3'])
        PubSubAZs = config.templateParameterValues['PubSubAZs3']
        PrivSub = config.templateParameterValues['PrivSub3']
        PrivSize = int(config.templateParameterValues['PrivSize3'])
        PrivSubAZs = config.templateParameterValues['PrivSubAZs3']
        NatGW = config.templateParameterValues['NatGW3']
        action = stack.vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW)
        config.logger.info('Response: {}'.format(action))
        del config.fragment['Outputs']
        action = {}
        action["statusCode"] = "200"
        action["body"] = config.json.dumps('Template Update Success!')
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["body"] = str(e)
        config.logger.info('Response: {}'.format(action))
    return action
