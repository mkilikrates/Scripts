import config
import gateway
import securitygroup
import createiamrole
import createinstprof
import launchtemplate
import autoscalegroup
import customresource
bgp = 0
def main():
    try:
        vpntype = config.templateParameterValues['vpntype']
        gwid = config.templateParameterValues['gwid']
        peerip = config.templateParameterValues['peerip']
        peercert = config.templateParameterValues['peercert']
        peername = config.templateParameterValues['peername']
        vpnopt = config.templateParameterValues['vpnopt']
        peerregion = {'Ref': 'peerregion'}
        localasn = {'Ref': 'localasn'}
        peerasn = {'Ref': 'peerasn'}
        InstNumb = {'Ref': 'InstNumb'}
        tgwdesc = {'Ref': 'tgwdesc'}
        autoacceptshrdattach = {'Ref': 'autoacceptshrdattach'}
        defrtassoc = {'Ref': 'defrtassoc'}
        defrtprop = {'Ref': 'defrtprop'}
        dnssup = {'Ref': 'dnssup'}
        multicastsup = {'Ref': 'multicastsup'}
        ecmpsup = {'Ref': 'ecmpsup'}
        VPC = config.templateParameterValues['VPC']
        Subnet = config.templateParameterValues['Subnet']
        SecurityGroup = config.templateParameterValues['SecurityGroup']
        SGAction = config.templateParameterValues['SGAction']
        ASGAction = config.templateParameterValues['ASGAction']
        SGSRC = config.templateParameterValues['SGSRC']
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
        if config.templateParameterValues['localasn'] != 0 and config.templateParameterValues['localasn'] != 0:
            bgp = 1
        if vpntype != 'Software VPN':
            if peerip.startswith('cgw-'):
                cgw = {'Ref' : peerip}
                dep = [peerip]
            elif peercert != '' and peerip == 'New':
                keylist = { 'Version' : 'V0.0.4', 'CustomerGatewayCert' : { 'CGWName' : peername, 'Region' : config.region, 'CGWASN' : peerasn, 'CertificateArn' : peercert } }
                action = customresource.create('CustomerGatewayCert','arn:aws:lambda:eu-west-1:778501541840:function:CloudFormationCustomResources-CustResFunc-242OKZQ449P0','',keylist)
                cgw = { "Fn::GetAtt" : ["CustomerGatewayCert", "CGWID" ] }
                dep = ['CustomerGatewayCert']
            elif peerip == 'New' and peercert == '':
                cgw = {'Ref' : peerip}
                dep = [peerip]
                keylist = { 'Version' : 'V0.0.2', 'AllocateAddress' : { 'Region' : peerregion, 'Domain' : 'vpc' } }
                action = customresource.create('CGWAddr','arn:aws:lambda:eu-west-1:778501541840:function:CloudFormationCustomResources-CustResFunc-242OKZQ449P0','',keylist)
                cgwip = { "Fn::GetAtt" : ["CGWAddr", "PublicIp" ] }
                dep = ['CGWAddr']
                action = gateway.cgw('CGW',peerasn,cgwip,'ipsec.1',bgp,dep)
                cgw = {'Ref' : 'CGW'}
                dep = ['CGW']
            else:
                action = gateway.cgw('CGW',peerasn,peerip,'ipsec.1',bgp,dep)
                cgw = {'Ref' : 'CGW'}
                dep = ['CGW']
            if vpntype == 'VGW' and gwid == 'New':
                action = gateway.vgw('VGW',localasn,tgwdesc,'ipsec.1',bgp,'')
                mygw = {'Ref' : 'VGW'}
                dep.append('VGW')
            if vpntype == 'TGW' and gwid == 'New':
                action = gateway.tgw('TGW',localasn,tgwdesc,bgp,autoacceptshrdattach,defrtassoc,defrtprop,dnssup,multicastsup,ecmpsup,'')
                mygw = {'Ref' : 'TGW'}
                dep.append('TGW')
            if gwid.startswith('vgw-') or gwid.startswith('tgw-'):
                mygw = {'Ref' : gwid}
                dep.append(mygw)
            if vpnopt == 'default':
                action = gateway.vpn('VPN',cgw,bgp,mygw,vpntype,dep)
            else:
                myvpnopts = {}
                vpnaccel = config.templateParameterValues['vpnaccel']
                vpnipfamily = config.templateParameterValues['vpnipfamily']
                myvpnopts['EnableAcceleration'] = {}
                myvpnopts['EnableAcceleration'] = vpnaccel
                myvpnopts['StaticRoutesOnly'] = {}
                if bgp == 0:
                    myvpnopts['StaticRoutesOnly'] = 'True'
                else:
                    myvpnopts['StaticRoutesOnly'] = 'False'
                myvpnopts['TunnelInsideIpVersion'] = {}
                myvpnopts['TunnelInsideIpVersion'] = vpnipfamily
                myvpnopts['TunnelOptions'] = []
                for i in range (2):
                    myvpnopts['TunnelOptions'].append({})
                    if config.templateParameterValues['tunnel' + str(i) + 'insidecidrv4'] !='':
                        myvpnopts['TunnelOptions'][i]['TunnelInsideCidr'] = {}
                        myvpnopts['TunnelOptions'][i]['TunnelInsideCidr'] = config.templateParameterValues['tunnel' + i + 'insidecidrv4']
                    if config.templateParameterValues['tunnel' + str(i) + 'insidecidrv6'] !='':
                        myvpnopts['TunnelOptions'][i]['TunnelInsideIpv6Cidr'] = {}
                        myvpnopts['TunnelOptions'][i]['TunnelInsideIpv6Cidr'] = config.templateParameterValues['tunnel' + i + 'insidecidrv6']
                    if config.templateParameterValues['tunnel' + str(i) + 'sharedkey'] !='':
                        myvpnopts['TunnelOptions'][i]['PreSharedKey'] = {}
                        myvpnopts['TunnelOptions'][i]['PreSharedKey'] = config.templateParameterValues['tunnel' + i + 'sharedkey']
                    if config.templateParameterValues['tunnelph1lifetime'] != '':
                        myvpnopts['TunnelOptions'][i]['Phase1LifetimeSeconds'] = {}
                        myvpnopts['TunnelOptions'][i]['Phase1LifetimeSeconds'] = config.templateParameterValues['tunnelph1lifetime']
                    if config.templateParameterValues['tunnelph2lifetime'] != '':
                        myvpnopts['TunnelOptions'][i]['Phase2LifetimeSeconds'] = {}
                        myvpnopts['TunnelOptions'][i]['Phase2LifetimeSeconds'] = config.templateParameterValues['tunnelph2lifetime']
                    if config.templateParameterValues['tunnelrekeymarg'] != '':
                        myvpnopts['TunnelOptions'][i]['RekeyMarginTimeSeconds'] = {}
                        myvpnopts['TunnelOptions'][i]['RekeyMarginTimeSeconds'] = config.templateParameterValues['tunnelrekeymarg']
                    if config.templateParameterValues['tunnelrekeyfuzz'] != '':
                        myvpnopts['TunnelOptions'][i]['RekeyFuzzPercentage'] = {}
                        myvpnopts['TunnelOptions'][i]['RekeyFuzzPercentage'] = config.templateParameterValues['tunnelrekeyfuzz']
                    if config.templateParameterValues['tunnelreplaywin'] != '':
                        myvpnopts['TunnelOptions'][i]['ReplayWindowSize'] = {}
                        myvpnopts['TunnelOptions'][i]['ReplayWindowSize'] = config.templateParameterValues['tunnelreplaywin']
                    if config.templateParameterValues['tunneldpdtimeout'] != '':
                        myvpnopts['TunnelOptions'][i]['DPDTimeoutSeconds'] = {}
                        myvpnopts['TunnelOptions'][i]['DPDTimeoutSeconds'] = config.templateParameterValues['tunneldpdtimeout']
                    if config.templateParameterValues['tunneldpdact'] != '':
                        myvpnopts['TunnelOptions'][i]['DPDTimeoutAction'] = {}
                        myvpnopts['TunnelOptions'][i]['DPDTimeoutAction'] = config.templateParameterValues['tunneldpdact']
                    if config.templateParameterValues['tunnelencalg'] != '':
                        myvpnopts['TunnelOptions'][i]['Phase1EncryptionAlgorithms'] = []
                        myvpnopts['TunnelOptions'][i]['Phase1EncryptionAlgorithms'].append({'Value' : config.templateParameterValues['tunnelencalg']})
                        myvpnopts['TunnelOptions'][i]['Phase2EncryptionAlgorithms'] = []
                        myvpnopts['TunnelOptions'][i]['Phase2EncryptionAlgorithms'].append({'Value' : config.templateParameterValues['tunnelencalg']})
                    if config.templateParameterValues['tunnelintalg'] != '':
                        myvpnopts['TunnelOptions'][i]['Phase1IntegrityAlgorithms'] = []
                        myvpnopts['TunnelOptions'][i]['Phase1IntegrityAlgorithms'].append({'Value' : config.templateParameterValues['tunnelintalg']})
                        myvpnopts['TunnelOptions'][i]['Phase2IntegrityAlgorithms'] = []
                        myvpnopts['TunnelOptions'][i]['Phase2IntegrityAlgorithms'].append({'Value' : config.templateParameterValues['tunnelintalg']})
                    if config.templateParameterValues['tunneldhg'] != '':
                        myvpnopts['TunnelOptions'][i]['Phase1DHGroupNumbers'] = []
                        myvpnopts['TunnelOptions'][i]['Phase1DHGroupNumbers'].append({'Value' : config.templateParameterValues['tunneldhg']})
                        myvpnopts['TunnelOptions'][i]['Phase2DHGroupNumbers'] = []
                        myvpnopts['TunnelOptions'][i]['Phase2DHGroupNumbers'].append({'Value' : config.templateParameterValues['tunneldhg']})
                    if config.templateParameterValues['tunnelikev'] != '':
                        myvpnopts['TunnelOptions'][i]['IKEVersions'] = []
                        myvpnopts['TunnelOptions'][i]['IKEVersions'].append({'Value' : config.templateParameterValues['tunnelikev']})
                    if config.templateParameterValues['tunnelstartact'] != '':
                        myvpnopts['TunnelOptions'][i]['StartupAction'] = {}
                        myvpnopts['TunnelOptions'][i]['StartupAction'] = config.templateParameterValues['tunnelstartact']
                myvpnopts['LocalIpv4NetworkCidr'] = {}
                myvpnopts['LocalIpv4NetworkCidr'] = '0.0.0.0/0'
                myvpnopts['RemoteIpv4NetworkCidr'] = {}
                myvpnopts['RemoteIpv4NetworkCidr'] = '0.0.0.0/0'
                if vpnipfamily == 'ipv6':
                    myvpnopts['LocalIpv6NetworkCidr'] = {}
                    myvpnopts['LocalIpv6NetworkCidr'] = '::/0'
                    myvpnopts['RemoteIpv6NetworkCidr'] = {}
                    myvpnopts['RemoteIpv6NetworkCidr'] = '::/0'
                keylist = { 'Version' : 'V0.0.3', 'VPNConn' : { 'Customer-Gateway-Id' : cgw, 'Gateway-Type' : vpntype, 'Gateway-Id' : mygw, 'VPNOptions' : myvpnopts} }
                action = customresource.create('VPNConn','arn:aws:lambda:eu-west-1:778501541840:function:CloudFormationCustomResources-CustResFunc-242OKZQ449P0','',keylist)
        else:
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
            action = launchtemplate.create(Hostname,InstType,LatestAmiId,sg,InstProfName,Keyname,usrdata,'No','')
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
