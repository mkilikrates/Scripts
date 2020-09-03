import config
import createsecuritygroup
import securitygrouprule
import createiamrole
import createinstprof
import createlaunchtemplate
import createautoscalegroup
def main():
    try:
        VPC = config.templateParameterValues['VPC']
        Subnet = config.templateParameterValues['Subnet']
        SecurityGroup = config.templateParameterValues['SecurityGroup']
        SGAction = config.templateParameterValues['SGAction']
        SGSRC = config.templateParameterValues['SGSRC']
        PublicIP = config.templateParameterValues['PublicIP']
        UpdateDNS = config.templateParameterValues['UpdateDNS']
        HostedZones = config.templateParameterValues['HostedZones']
        InstType = config.templateParameterValues['InstType']
        InstNumb = config.templateParameterValues['InstNumb']
        Hostname = config.templateParameterValues['Hostname']
        LatestAmiId = config.templateParameterValues['LatestAmiId']
        InstProfName = config.templateParameterValues['InstProfName']
        InstProfAct = config.templateParameterValues['InstProfAct']
        MgtPol = config.templateParameterValues['MgtPol']
        Keyname = config.templateParameterValues['Keyname']
        usrdata = config.templateParameterValues['usrdata']
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        netsrc = []
        if ',' in SGSRC:
            netsrc = list(SGSRC.split(','))
        else:
            netsrc.append(SGSRC)
        if SGAction == 'Create SG':
            action = createsecuritygroup.main(VPC,Hostname)
            config.logger.info('Response: {}'.format(action))
            for src in netsrc:
                if src.startswith('pl-'):
                    action = securitygrouprule.addingress('SecG' + Hostname,src,'SourcePrefixListId','-1','','','')
                    config.logger.info('Response: {}'.format(action))
                elif src == 'zoneprefix':
                    with open('zonemap.cfg') as zonefile:
                        zonemap = config.json.load(zonefile)
                        srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                        action = securitygrouprule.addingress('SecG' + Hostname,srcprefix,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                else:
                    ip = config.IPNetwork(src)
                    if ip.version == 4:
                        action = securitygrouprule.addingress('SecG' + Hostname,str(ip),'CidrIp','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    if ip.version == 6:
                        action = securitygrouprule.addingress('SecG' + Hostname,str(ip),'CidrIpv6','-1','','','')
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag('IAMRole' + Hostname,'ec2.amazonaws.com',MgtPol)
                config.logger.info('Response: {}'.format(action))
                action = createinstprof.main('InstProf' + Hostname,'IAMRole' + Hostname,'yes')
                config.logger.info('Response: {}'.format(action))
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SecG' + Hostname,'InstProf' + Hostname,Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SecG' + Hostname,'InstProfName',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SecG' + Hostname,'',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
        elif SGAction == 'Update SG':
            for src in netsrc:
                if src.startswith('pl-'):
                    action = securitygrouprule.addingress(SecurityGroup[0],src,'SourcePrefixListId','-1','','','')
                    config.logger.info('Response: {}'.format(action))
                elif src == 'zoneprefix':
                    with open('zonemap.cfg') as zonefile:
                        zonemap = config.json.load(zonefile)
                        srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                        action = securitygrouprule.addingress(SecurityGroup[0],srcprefix,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                else:
                    ip = config.IPNetwork(src)
                    if ip.version == 4:
                        action = securitygrouprule.addingress(SecurityGroup[0],ip,'CidrIp','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    if ip.version == 6:
                        action = securitygrouprule.addingress(SecurityGroup[0],ip,'CidrIpv6','-1','','','')
                        config.logger.info('Response: {}'.format(action))
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag('IAMRole' + Hostname,'ec2.amazonaws.com',MgtPol)
                config.logger.info('Response: {}'.format(action))
                action = createinstprof.main('InstProf' + Hostname,'IAMRole' + Hostname,'yes')
                config.logger.info('Response: {}'.format(action))
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'InstProf' + Hostname,Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'InstProfName',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
        else:
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag('IAMRole' + Hostname,'ec2.amazonaws.com',MgtPol)
                config.logger.info('Response: {}'.format(action))
                action = createinstprof.main('InstProf' + Hostname,'IAMRole' + Hostname,'yes')
                config.logger.info('Response: {}'.format(action))
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'InstProf' + Hostname,Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'InstProfName',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,SecurityGroup,'',Keyname,usrdata,PublicIP)
                config.logger.info('Response: {}'.format(action))
        action = createautoscalegroup.main(Hostname,'',InstNumb,'','LT' + Hostname,'',InstNumb,InstNumb,Subnet)
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
