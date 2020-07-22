import config
import createvpc
import createvpc6
import createdhcpoptions
import createinternetgw
import createroutetable
import route
import createsubnet
import createnatinstance
import createegressgw

def vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW):
    try:
        config.logger.info('Create VPC ' + vpcname + ' : {0}\nDualStack: {1}'.format(VpcCidr,UpdateDNS))
        action = createvpc.main(vpcname,VpcCidr,UpdateDNS,PrivHZ)
        config.logger.info('Response: {}'.format(action))
        cidrvpc = config.IPNetwork(VpcCidr)
        if DualStack == 'Yes':
            action = createvpc6.main(vpcname)
            config.logger.info('Response: {}'.format(action))
        if UpdateDNS == 'Yes':
            action = createdhcpoptions.main(vpcname,PrivHZ)
            config.logger.info('Response: {}'.format(action))
        if PubSub == 'Yes':
            action = createinternetgw.main(vpcname,DualStack)
            config.logger.info('Response: {}'.format(action))
            action = createroutetable.main(vpcname,'Pub',DualStack)
            config.logger.info('Response: {}'.format(action))
            action = route.addv4('PubDefaultIpv4','0.0.0.0/0','RTPub' + vpcname,'GatewayId','IGW' + vpcname)
            config.logger.info('Response: {}'.format(action))
            if DualStack == 'Yes':
                action = route.addv6('PubDefaultIpv6','::/0','RTPub' + vpcname,'GatewayId','IGW' + vpcname)
                config.logger.info('Response: {}'.format(action))
            subnets = list(cidrvpc.subnet(PubSize))
            maxsub = len(subnets)
            i=0 # Counter to be used in iterations
            #cidrblock=VpcCidr.split('/',2)[1]
            #ipbits=32-int(PubSize)
            #ipaddr=(2**ipbits)
            for id in PubSubAZs:
                if DualStack == 'Yes':
                    action = createsubnet.main(vpcname,'Pub' + vpcname,str(subnets[i]),id,DualStack,'IPv6',i,'RTPub' + vpcname)
                    config.logger.info('Response: {}'.format(action))
                else:
                    action = createsubnet.main(vpcname,'Pub' + vpcname,str(subnets[i]),id,DualStack,'Pub',i,'RTPub' + vpcname)
                    config.logger.info('Response: {}'.format(action))
                i=i+1
        if PrivSub == 'Yes':
            subnets = list(cidrvpc.subnet(PrivSize))
            maxsub = len(subnets)
            if DualStack == 'Yes':
                action = createegressgw.main(vpcname)
                config.logger.info('Response: {}'.format(action))
            if NatGW == 'Single' and PubSub == 'Yes':
                i=maxsub-1
                i6=255
                action = createroutetable.main(vpcname,'Priv',DualStack)
                config.logger.info('Response: {}'.format(action))
                action = createnatinstance.main(vpcname,'Pub' + vpcname,PubSubAZs[0])
                config.logger.info('Response: {}'.format(action))
                action = route.addv4('PrivDefaultIpv4' + vpcname,'0.0.0.0/0','RTPriv' + vpcname,'NatGatewayId','NATgwAZ' + vpcname + PubSubAZs[0][-2:])
                config.logger.info('Response: {}'.format(action))
                if DualStack == 'Yes':
                    action = route.addv6('PrivDefaultIpv6' + vpcname,'::/0','RTPriv' + vpcname,'EgressOnlyInternetGatewayId','EgressGW' + vpcname)
                    config.logger.info('Response: {}'.format(action))
                for id in PrivSubAZs:
                    if DualStack == 'Yes':
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'IPv6',i6,'RTPriv' + vpcname)
                        config.logger.info('Response: {}'.format(action))
                    else:
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'None',i6,'RTPriv' + vpcname)
                        config.logger.info('Response: {}'.format(action))
                    i=i-1
                    i6=i6-1
            elif NatGW == 'PerAz' and PubSub == 'Yes':
                i=maxsub-1
                i6=255
                for id in PrivSubAZs:
                    action = createroutetable.main(vpcname,'Priv' + id[-2:],DualStack)
                    config.logger.info('Response: {}'.format(action))
                    action = createnatinstance.main(vpcname,'Pub' + vpcname,id)
                    config.logger.info('Response: {}'.format(action))
                    action = route.addv4('Priv' + vpcname + id[-2:] + 'DefaultIpv4','0.0.0.0/0','RTPriv' + id[-2:] + vpcname,'NatGatewayId','NATgwAZ' + vpcname + id[-2:])
                    config.logger.info('Response: {}'.format(action))
                    if DualStack == 'Yes':
                        action = route.addv6('PrivDefaultIpv6' + vpcname + id[-2:],'::/0','RTPriv' + id[-2:] + vpcname,'EgressOnlyInternetGatewayId','EgressGW' + vpcname)
                        config.logger.info('Response: {}'.format(action))
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'IPv6',i6,'RTPriv' + id[-2:] + vpcname)
                        config.logger.info('Response: {}'.format(action))
                    else:
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'None',i6,'RTPriv' + id[-2:] + vpcname)
                        config.logger.info('Response: {}'.format(action))
                    i=i-1
                    i6=i6-1
            else:
                i=maxsub-1
                i6=255
                for id in PrivSubAZs:
                    if DualStack == 'Yes':
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'IPv6',i6,'None')
                        config.logger.info('Response: {}'.format(action))
                    else:
                        action = createsubnet.main(vpcname,'Priv' + vpcname,str(subnets[i]),id,DualStack,'None',i6,'None')
                        config.logger.info('Response: {}'.format(action))
                    i=i-1
                    i6=i6-1
        action = {}
        action["statusCode"] = "200"
        action["body"] = config.json.dumps('VPC Template' + vpcname + ' Update Success!')
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


