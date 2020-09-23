import config
def create(VPC,name):
    try:
        config.fragment['Resources']['SecG' + name] = {}
        config.fragment['Resources']['SecG' + name]['Type'] = 'AWS::EC2::SecurityGroup'
        config.fragment['Resources']['SecG' + name]['Properties'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupName'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupName'] = 'SecG' + name
        config.fragment['Resources']['SecG' + name]['Properties']['GroupDescription'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupDescription'] = 'SecG' + name
        config.fragment['Resources']['SecG' + name]['Properties']['VpcId'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['VpcId'] = VPC
        config.fragment['Outputs']['SecG' + name] = {}
        config.fragment['Outputs']['SecG' + name]['Description'] = {}
        config.fragment['Outputs']['SecG' + name]['Description'] = 'Security Group ID' + name
        config.fragment['Outputs']['SecG' + name]['Value'] = {}
        config.fragment['Outputs']['SecG' + name]['Value'] = {'Ref': 'SecG' + name}
        config.fragment['Outputs']['SecG' + name]['Export'] = {}
        config.fragment['Outputs']['SecG' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'SecG' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Security Group ID SG' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def addingress(sg,src,srctype,proto,fromport,toport,desc):
    # Where:
    # sg = Security Group ID
    # src = Source (CIDR, PrefixList or SecurityGroupID)
    # srctype = Source type to be used (CidrIp, CidrIpv6, SourcePrefixListId, SourceSecurityGroupId:<SourceSecurityGroupOwnerId>)
    # proto = Protocol number or -1 for ALL
    # fromport = first port number or range for the TCP and UDP protocols, or an ICMP/ICMPv6 type number. -1 for ALL icmp
    # toport = end port number or range for the TCP and UDP protocols, or an ICMP/ICMPv6 type number. -1 for ALL icmp
    # desc = Description
    try:
        srcname = src
        if ':' in srcname:
            srcname = srcname.replace(':','')
        if '-' in srcname:
            srcname = srcname.replace('-','')
        if '/' in srcname:
            srcname = srcname.replace('/','')
        if '.' in srcname:
            srcname = srcname.replace('.','')
        if sg.startswith('sg-'):
            sgname = sg.replace('-','')
        else:
            sgname = sg
        config.fragment['Resources']['SGRule' + sgname + srcname] = {}
        config.fragment['Resources']['SGRule' + sgname + srcname]['Type'] = 'AWS::EC2::SecurityGroupIngress'
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties'] = {}
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['GroupId'] = {}
        if sg.startswith('sg-'):
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['GroupId'] = sg
        else:
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['GroupId'] = { "Ref": sg }
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['IpProtocol'] = {}
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['IpProtocol'] = proto
        if fromport != '':
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['FromPort'] = {}
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['FromPort'] = fromport
        if toport != '':
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['ToPort'] = {}
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['ToPort'] = fromport
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties'][srctype] = {}
        config.fragment['Resources']['SGRule' + sgname + srcname]['Properties'][srctype] = src
        if desc != '':
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['Description'] = {}
            config.fragment['Resources']['SGRule' + sgname + srcname]['Properties']['Description'] = desc
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Rule Add Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
