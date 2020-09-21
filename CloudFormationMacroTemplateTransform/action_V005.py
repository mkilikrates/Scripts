import config
import securitygroup
import simpleAD
import r53resolver
import customresource
def main():
    try:
        if len(config.templateParameterValues['SubnetAD']) >2:
            response["statusCode"] = "400"
            response["body"] = config.json.dumps('Simple AD Allow only 2 subnets!')
            return response
        else:
            name = {'Ref': 'SimpleADName'}
            if config.templateParameterValues['Alias'] != '':
                alias = {'Ref': 'Alias'}
            else:
                alias = ''
            recname = config.templateParameterValues['NetbiosNm']
            desc = {'Ref': 'DescAD'}
            sso = {'Ref': 'SSO'}
            pwd = {'Ref': 'SimpleADPwd'}
            netb = {'Ref': 'NetbiosNm'}
            size = {'Ref': 'Size'}
            subad = {'Ref': 'SubnetAD'}
            vpc = {'Ref': 'VPC'}
            r53endname = config.templateParameterValues['R53EndPtName']
            subr53end = config.templateParameterValues['SubnetR53End']
            sgr53end = config.templateParameterValues['SecGR53End']
            sgr53endact = config.templateParameterValues['SecGR53EndAct']
            sgr53endsrc = config.templateParameterValues['SecGR53EndSrc']
            config.fragment['Resources'] = {}
            config.fragment['Outputs'] = {}
            action = simpleAD.create(recname,name,alias,desc,sso,pwd,netb,size,subad,vpc,'')
            config.logger.info('Response: {}'.format(action))
            netsrc = []
            if ',' in sgr53endsrc:
                netsrc = list(sgr53endsrc.split(','))
            else:
                netsrc.append(sgr53endsrc)
            if sgr53endact == 'Create SG':
                action = securitygroup.create(vpc,r53endname)
                config.logger.info('Response: {}'.format(action))
                for src in netsrc:
                    if src.startswith('pl-'):
                        action = securitygroup.addingress('SecG' + r53endname,src,'SourcePrefixListId','-1','','','')
                        config.logger.info('Response: {}'.format(action))
                    elif src == 'zoneprefix':
                        with open('zonemap.cfg') as zonefile:
                            zonemap = config.json.load(zonefile)
                            srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
                            action = securitygroup.addingress('SecG' + r53endname,srcprefix,'SourcePrefixListId','-1','','','')
                            config.logger.info('Response: {}'.format(action))
                    else:
                        ip = config.IPNetwork(src)
                        if ip.version == 4:
                            action = securitygroup.addingress('SecG' + r53endname,str(ip),'CidrIp','-1','','','')
                            config.logger.info('Response: {}'.format(action))
                        if ip.version == 6:
                            action = securitygroup.addingress('SecG' + r53endname,str(ip),'CidrIpv6','-1','','','')
                sg = [{'Ref': 'SecG' + r53endname}]
                action = r53resolver.createendpoint(r53endname,'OUTBOUND',sg,subr53end,'SimpleAD' + recname)
                config.logger.info('Response: {}'.format(action))
            elif sgr53endact == 'Update SG':
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
                sg = sgr53end
                action = r53resolver.createendpoint(r53endname,'OUTBOUND',sg,subr53end,'SimpleAD' + recname)
                config.logger.info('Response: {}'.format(action))
            else:
                sg = sgr53end
                action = r53resolver.createendpoint(r53endname,'OUTBOUND',sg,subr53end,'SimpleAD' + recname)
                config.logger.info('Response: {}'.format(action))
            dep = ['SimpleAD' + recname]
            keylist = { 'Version' : 'V0.0.1', 'DirectoryId' : {'Ref' : 'SimpleAD' + recname } }
            action = customresource.create('namesrv','arn:aws:lambda:eu-west-1:778501541840:function:CloudFormationCustomResources-CustResFunc-242OKZQ449P0',dep,keylist)
            config.logger.info('Response: {}'.format(action))
            dep = ['SimpleAD' + recname,'R53ResEnd' + r53endname]
            dns = { "Ref" : "namesrv" }
            action = r53resolver.createrule(r53endname + recname,name,'R53ResEnd' + r53endname,'FORWARD',dns,dep)
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
