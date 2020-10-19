import config
import securitygroup
import createiamrole
import createinstprof
import launchtemplate
import autoscalegroup
def main():
    try:
        VPC = config.templateParameterValues['VPC']
        Subnet = config.templateParameterValues['Subnet']
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
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        netsrc = []
        if ',' in SGSRC:
            netsrc = list(SGSRC.split(','))
        else:
            netsrc.append(SGSRC)
        if SGAction == 'Create SG':
            action = securitygroup.create(VPC,Hostname)
            config.logger.info('Response: {}'.format(action))
            for src in netsrc:
                if src.startswith('pl-'):
                    action = securitygroup.addingress('SecG' + Hostname,src,'SourcePrefixListId','-1','','','')
                    config.logger.info('Response: {}'.format(action))
                elif src == 'zoneprefix':
                    with open('zonemap.cfg') as zonefile:
                        zonemap = config.json.load(zonefile)
                        srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                        action = securitygroup.addingress('SecG' + Hostname,srcprefix,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                else:
                    ip = config.IPNetwork(src)
                    if ip.version == 4:
                        action = securitygroup.addingress('SecG' + Hostname,str(ip),'CidrIp','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    if ip.version == 6:
                        action = securitygroup.addingress('SecG' + Hostname,str(ip),'CidrIpv6','-1','','','')
            srcsg = {'Ref': 'SecG' + Hostname}
            action = securitygroup.addingress('SecG' + Hostname,srcsg,'SourceSecurityGroupId','-1','','','')
            sg = [ { 'Fn::GetAtt' : [ 'SecG' + Hostname, 'GroupId' ] } ]
        elif SGAction == 'Update SG':
            for src in netsrc:
                if src.startswith('pl-'):
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
            sg = [ {'Ref': 'SecurityGroup'} ]
        elif SGAction == 'Use SG with no change':
            sg = [ {'Ref': 'SecurityGroup'} ]
        if InstProfAct == 'No Role':
            InstProfName = ''
        elif InstProfAct == 'Create New Role':
            action = createiamrole.manag('IAMRole' + Hostname,'ec2.amazonaws.com',MgtPol)
            config.logger.info('Response: {}'.format(action))
            action = createinstprof.main('InstProf' + Hostname,'IAMRole' + Hostname,'yes')
            config.logger.info('Response: {}'.format(action))
            InstProfName = {'Ref': 'InstProf' + Hostname}
        elif InstProfAct == 'Use Existent Role':
            InstProfName = {'Ref': 'InstProfName'}
        action = launchtemplate.create(Hostname,InstType,LatestAmiId,sg,InstProfName,Keyname,usrdata,PublicIP,'')
        config.logger.info('Response: {}'.format(action))
        ltemp = 'LT' + Hostname
        dep = ['LT' + Hostname]
        action = autoscalegroup.create(Hostname,'',InstNumb,'',ltemp,'',InstMin,InstMax,Subnet,dep)
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
