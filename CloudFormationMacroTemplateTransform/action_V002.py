import config
import createsecuritygroup
def main():
    try:
        VPC = config.templateParameterValues['VPC']
        Subnet = config.templateParameterValues['Subnet']
        SecurityGroup = config.templateParameterValues['SecurityGroup']
        SGAction = config.templateParameterValues['SGAction']
        SGSRC = int(config.templateParameterValues['UpdateDNS'])
        UpdateDNS = config.templateParameterValues['PubSubAZs']
        HostedZones = config.templateParameterValues['HostedZones']
        InstType = int(config.templateParameterValues['InstType'])
        InstNumb = config.templateParameterValues['InstNumb']
        Hostname = config.templateParameterValues['Hostname']
        LatestAmiId = config.templateParameterValues['LatestAmiId']
        InstProfName = config.templateParameterValues['InstProfName']
        InstProfAct = config.templateParameterValues['InstProfAct']
        MgtPol = config.templateParameterValues['MgtPol']
        Keyname = config.templateParameterValues['Keyname']
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        if ',' in tag['SGSRC']:
            netsrc = list(SGSRC.split(','))
        else:
            netsrc.append(tag['SGSRC'])
        if SGAction == 'Create SG':
            action = createsecuritygroup.main(VPC,Hostname)
            config.logger.info('Response: {}'.format(action))
            for src in netsrc:
                if src.startswith('pl-'):
                    action = securitygrouprule.addingress('SG' + Hostname,src,'SourcePrefixListId','-1','','','')
                else:
                    ip = IPNetwork(src)
                    if ip.version == 4:
                        action = securitygrouprule.addingress('SG' + Hostname,ip,'CidrIp','-1','','','')
                    if ip.version == 6:
                        action = securitygrouprule.addingress('SG' + Hostname,ip,'CidrIpv6','-1','','','')
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag(InstProfName,'ec2.amazonaws.com',MgtPol)
                action = createinstprof.main(InstProfName,InstProfIamRole + 'Role','yes')
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,'',Keyname)
        elif SGAction == 'Update SG':
            for src in netsrc:
                if src.startswith('pl-'):
                    action = securitygrouprule.addingress(SecurityGroup,src,'SourcePrefixListId','-1','','','')
                else:
                    ip = IPNetwork(src)
                    if ip.version == 4:
                        action = securitygrouprule.addingress(SecurityGroup,ip,'CidrIp','-1','','','')
                    if ip.version == 6:
                        action = securitygrouprule.addingress(SecurityGroup,ip,'CidrIpv6','-1','','','')
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag(InstProfName,'ec2.amazonaws.com',MgtPol)
                action = createinstprof.main(InstProfName,InstProfIamRole + 'Role','yes')
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,'',Keyname)
        else:
            if InstProfAct == 'Create New Role':
                action = createiamrole.manag(InstProfName,'ec2.amazonaws.com',MgtPol)
                action = createinstprof.main(InstProfName,InstProfIamRole + 'Role','yes')
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            elif InstProfAct == 'Use Existent Role':
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,InstProfName,Keyname)
            else:
                action = createlaunchtemplate.main(Hostname,InstType,LatestAmiId,'SG' + Hostname,'',Keyname)

##### continuar
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

