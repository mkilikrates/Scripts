import config
import stack
import elbv2

def main():
    try:
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        UpdateDNS = 'No'
        PrivHZ = ''
        # create GW VPC 
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
        SecurityGroup = config.templateParameterValues['SecurityGroup']
        SGAction = config.templateParameterValues['SGAction']
        ASGAction = config.templateParameterValues['ASGAction']
        SGSRC = config.templateParameterValues['SGSRC']
        PublicIP = config.templateParameterValues['PublicIP']
        UpdateDNS = config.templateParameterValues['UpdateDNS']
        HostedZones = config.templateParameterValues['HostedZones']
        InstType = {'Ref': 'InstType'}
        InstNumb = {'Ref': 'InstNumb'}
        InstMin = {'Ref': 'InstMin'}
        InstMax = {'Ref': 'InstMax'}
        Hostname = config.templateParameterValues['Hostname']
        LatestAmiId = {'Ref': 'LatestAmiId'}
        InstProfAct = config.templateParameterValues['InstProfAct']
        MgtPol = config.templateParameterValues['MgtPol']
        Keyname = config.templateParameterValues['Keyname']
        usrdata = config.templateParameterValues['usrdata']
        action = stack.vpc(UpdateDNS,PrivHZ,vpcname,DualStack,VpcCidr,PubSub,PubSize,PubSubAZs,PrivSub,PrivSize,PrivSubAZs,NatGW)
        config.logger.info('Response: {}'.format(action))
        # find subnets to deploy GW
        Subnet = []
        for id in PubSubAZs:
            sub.append("Ref" : vpcname + name + 'SubAZ' + AZ[-2:])
        # create GWLB
        action = elbv2.lb('GWLB','dualstack','gateway',Subnet,'','','')
        config.logger.info('Response: {}'.format(action))
        netsrc = []
        if ',' in SGSRC:
            netsrc = list(SGSRC.split(','))
        else:
            netsrc.append(SGSRC)
        # create Security Group for GW
        if SGAction == 'Create SG':
            vpcid = {"Ref" : 'Vpc' + vpcname }
            sgname = 'SGGW' + vpcname
            action = securitygroup.create(vpcid,sgname)
            config.logger.info('Response: {}'.format(action))
            for src in netsrc:
                # create Rules for adm GW
                if src.startswith('pl-'):
                    action = securitygroup.addingress(sgname,src,'SourcePrefixListId','-1','','','')
                    config.logger.info('Response: {}'.format(action))
                elif src == 'zoneprefix':
                    with open('zonemap.cfg') as zonefile:
                        zonemap = config.json.load(zonefile)
                        srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                        action = securitygroup.addingress(sgname,srcprefix,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                else:
                    ip = config.IPNetwork(src)
                    if ip.version == 4:
                        action = securitygroup.addingress(sgname,str(ip),'CidrIp','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    if ip.version == 6:
                        action = securitygroup.addingress(sgname,str(ip),'CidrIpv6','-1','','','')
            srcsg = {'Ref': sgname}
            # create Rules for GW works
            action = securitygroup.addingress(sgname,VpcCidr,'CidrIp','udp','6081','6081','Geneve')
            sg = [ { 'Fn::GetAtt' : [ sgname, 'GroupId' ] } ]
        elif SGAction == 'Update SG':
            for src in netsrc:
                if src.startswith('pl-'):
                    # create Rules for GW
                    action = securitygroup.addingress(SecurityGroup[0],src,'SourcePrefixListId','-1','','','')
                    config.logger.info('Response: {}'.format(action))
                elif src == 'zoneprefix':
                    with open('zonemap.cfg') as zonefile:
                        zonemap = config.json.load(zonefile)
                        srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                        action = securitygroup.addingress(SecurityGroup[0],srcprefix,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                else:
                    ip = config.IPNetwork(src)
                    if ip.version == 4:
                        action = securitygroup.addingress(SecurityGroup[0],ip,'CidrIp','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    if ip.version == 6:
                        action = securitygroup.addingress(SecurityGroup[0],ip,'CidrIpv6','-1','','','')
                        config.logger.info('Response: {}'.format(action))
            sg = {'Ref': 'SecurityGroup'}
        elif SGAction == 'Use SG with no change':
            sg = {'Ref': 'SecurityGroup'}
        if InstProfAct == 'No Role':
            InstProfName = ''
        elif InstProfAct == 'Create New Role':
            # create Instance Profile
            action = createiamrole.manag('IAMRole' + Hostname,'ec2.amazonaws.com',MgtPol)
            config.logger.info('Response: {}'.format(action))
            action = createinstprof.main('InstProf' + Hostname,'IAMRole' + Hostname,'yes')
            config.logger.info('Response: {}'.format(action))
            InstProfName = {'Ref': 'InstProf' + Hostname}
        elif InstProfAct == 'Use Existent Role':
            InstProfName = {'Ref': 'InstProfName'}
        # create GW Launch Template
        action = launchtemplate.create(Hostname,InstType,LatestAmiId,sg,InstProfName,Keyname,usrdata,PublicIP,'')
        config.logger.info('Response: {}'.format(action))
        ltemp = 'LT' + Hostname
        dep = ['LT' + Hostname]
        # create GW Target Group
        hcmatch = { "HttpCode" : "200–399" }
        hcheltc = 3
        hcunheltc = 3
        hctout = 5
        hcintv = 10
        hctgatt =''
        hctarg = ''
        dep = ['Vpc' + vpcname]
        action = elbv2.tgrp(Hostname,vpcid,'instance','GENEVE',6081,'HTTP','80','/',hcmatch,hcheltc,hcunheltc,hctout,hcintv,hctgatt,hctarg,dep)
        config.logger.info('Response: {}'.format(action))
        # create GW Auto Scale Group
        LB = { "Fn::GetAtt" : [ 'TGRP' + name, LoadBalancerArns ]  }
        dep = ['Vpc' + vpcname,'TGRP' + name]
        action = autoscalegroup.create(Hostname,'',InstNumb,'',ltemp,LB,InstMin,InstMax,Subnet,dep)
        config.logger.info('Response: {}'.format(action))
        if ASGAction == 'Yes':
            asgname = 'ASG' + Hostname
            ncapac = config.templateParameterValues['InstNumb']
            capac = 'DesiredCapacity:' + ncapac
            recr = {'Ref': 'AsgActStartRec'}
            dep = [asgname]
            action = autoscalegroup.schdact('startday',asgname,capac,'','',recr,dep)
            config.logger.info('Response: {}'.format(action))
            mincapac = config.templateParameterValues['InstMin']
            capac = 'DesiredCapacity:' + mincapac
            recr = {'Ref': 'AsgActStopRec'}
            action = autoscalegroup.schdact('stopday',asgname,capac,'','',recr,dep)
            config.logger.info('Response: {}'.format(action))
        # create LB Listener
        act = [ { "Type" : "forward" } ]
        action = elbv2.lst(Hostname,'','',act,LB,'','','','TGRP' + name)
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
