import config
def create(desc,authopt,authparam,clicertarn,cidr,loggrp,logstm,dns,sg,certarn,split,transp,vpc,port):
    # Where:
    # desc = description
    # authtype = authentication Type (certificate-authentication | directory-service-authentication | federated-authentication))
    # authparam = additional paremeter (DirectoryId, SAMLProviderArn)
    # clicertarn = ClientRootCertificateChainArn
    # cidr = ClientVPN CIDR
    # loggrp = CloudwatchLogGroup
    # logstm = CloudwatchLogStream
    # dns = DnsServers - List of nameservers
    # sg = SecurityGroupIds list
    # certarn = ServerCertificateArn - The ARN of the server certificate
    # split = Indicates whether split-tunnel is enabled
    # transp = transport (tcp | udp)
    # vpc = VpcId
    # port = VpnPort
    try:
        config.fragment['Resources']['CVPNE'] = {}
        config.fragment['Resources']['CVPNE']['Type'] = 'AWS::EC2::ClientVpnEndpoint'
        config.fragment['Resources']['CVPNE']['Properties'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['AuthenticationOptions'] = []
        if authopt == "Directory":
            config.fragment['Resources']['CVPNE']['Properties']['AuthenticationOptions'].append( { "ActiveDirectory" : {  "DirectoryId" : authparam }, "Type" : "directory-service-authentication" } )
        elif authopt == "Federated":
            config.fragment['Resources']['CVPNE']['Properties']['AuthenticationOptions'].append( { "FederatedAuthentication" : {  "SAMLProviderArn" : authparam }, "Type" : "federated-authentication" } )
        if clicertarn != '':
            config.fragment['Resources']['CVPNE']['Properties']['AuthenticationOptions'].append( { "MutualAuthentication" : {  "ClientRootCertificateChainArn" : clicertarn }, "Type" : "certificate-authentication" } )
        config.fragment['Resources']['CVPNE']['Properties']['ClientCidrBlock'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['ClientCidrBlock'] = cidr
        if loggrp != '' and logstm != '':
            config.fragment['Resources']['CVPNE']['Properties']['ConnectionLogOptions'] = {}
            config.fragment['Resources']['CVPNE']['Properties']['ConnectionLogOptions'] = { "CloudwatchLogGroup" : loggrp, "CloudwatchLogStream" : logstm, "Enabled" : "true" }
        config.fragment['Resources']['CVPNE']['Properties']['Description'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['Description'] = desc
        if dns != '':
            config.fragment['Resources']['CVPNE']['Properties']['DnsServers'] = []
            if ' ' in dns:
                dns = dns.replace(' ','')
            if ',' in dns:
                nameserver = list(dns.split(','))
            else:
                nameserver = []
                nameserver.append(dns)
            for ns in nameserver:
                config.fragment['Resources']['CVPNE']['Properties']['DnsServers'].append(ns)
        config.fragment['Resources']['CVPNE']['Properties']['SecurityGroupIds'] = []
        if ' ' in sg:
            sg = sg.replace(' ','')
        for seg in sg:
            config.fragment['Resources']['CVPNE']['Properties']['SecurityGroupIds'].append(seg)
        if certarn != '':
            config.fragment['Resources']['CVPNE']['Properties']['ServerCertificateArn'] = {}
            config.fragment['Resources']['CVPNE']['Properties']['ServerCertificateArn'] = certarn
        if split == "Yes":
            config.fragment['Resources']['CVPNE']['Properties']['SplitTunnel'] = {}
            config.fragment['Resources']['CVPNE']['Properties']['SplitTunnel'] = "True"

        config.fragment['Resources']['CVPNE']['Properties']['TagSpecifications'] = []
        config.fragment['Resources']['CVPNE']['Properties']['TagSpecifications'] = [ { 'ResourceType' : 'client-vpn-endpoint', 'Tags' : [ {'Key': 'Name', 'Value': { 'Ref': 'AWS::StackName' } } ] } ]
        config.fragment['Resources']['CVPNE']['Properties']['TransportProtocol'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['TransportProtocol'] = transp
        config.fragment['Resources']['CVPNE']['Properties']['VpcId'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['VpcId'] = vpc
        config.fragment['Resources']['CVPNE']['Properties']['VpnPort'] = {}
        config.fragment['Resources']['CVPNE']['Properties']['VpnPort'] = port
        config.fragment['Outputs']['CVPNE'] = {}
        config.fragment['Outputs']['CVPNE']['Description'] = 'Client VPN Endpoint'
        config.fragment['Outputs']['CVPNE']['Value'] = {'Ref': 'CVPNE'}
        config.fragment['Outputs']['CVPNE']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'CVPNE' ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('CVPNE Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response


def netass(vpne,sub):
    # Network Association
    # Where:
    # vpne = ClientVpnEndpointId
    # sub = SubnetId
    try:
        for subnet in sub:
            subname = subnet
            if ' ' in subname:
                subname = subname.replace(' ','')
            subname = subname.replace('-','')
            config.fragment['Resources']['CvpneAss' + subname] = {}
            config.fragment['Resources']['CvpneAss' + subname]['Type'] = 'AWS::EC2::ClientVpnTargetNetworkAssociation'
            config.fragment['Resources']['CvpneAss' + subname]['Properties'] = {}
            config.fragment['Resources']['CvpneAss' + subname]['Properties']['ClientVpnEndpointId'] = {}
            config.fragment['Resources']['CvpneAss' + subname]['Properties']['ClientVpnEndpointId'] = { "Ref": vpne }
            config.fragment['Resources']['CvpneAss' + subname]['Properties']['SubnetId'] = {}
            config.fragment['Resources']['CvpneAss' + subname]['Properties']['SubnetId'] = subnet
            config.fragment['Resources']['CvpneAss' + subname]['DependsOn'] = {}
            config.fragment['Resources']['CvpneAss' + subname]['DependsOn'] = 'CVPNE'
            config.fragment['Outputs']['CvpneAss' + subname] = {}
            config.fragment['Outputs']['CvpneAss' + subname]['Description'] = 'Client VPN Endpoint Association' + subnet
            config.fragment['Outputs']['CvpneAss' + subname]['Value'] = {'Ref': 'CvpneAss' + subname}
            config.fragment['Outputs']['CvpneAss' + subname]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'CvpneAss' + subname ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Cvpne Association Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def route(vpne,sub,cidr):
    # Network Association
    # Where:
    # vpne = ClientVpnEndpointId
    # sub = SubnetId
    # cidr = cidr list
    try:
        if ' ' in cidr:
            cidr = cidr.replace(' ','')
        if ',' in cidr:
            cidrlist = list(cidr.split(','))
        else:
            cidrlist = []
            cidrlist.append(cidr)
        for net in cidrlist:
            netname = net
            if ':' in netname:
                netname = netname.replace(':','')
            if '-' in netname:
                netname = netname.replace('-','')
            if '/' in netname:
                netname = netname.replace('/','')
            if '.' in netname:
                netname = netname.replace('.','')
                for subnet in sub:
                    subname = subnet
                    if ' ' in subname:
                        subname = subname.replace(' ','')
                    subname = subname.replace('-','')
                    config.fragment['Resources']['Cvpnerout' + netname + subname] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Type'] = 'AWS::EC2::ClientVpnRoute'
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['ClientVpnEndpointId'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['ClientVpnEndpointId'] = { "Ref": vpne }
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['Description'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['Description'] = 'Cvpne route' + net + ' via assoc. ' + subnet
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['DestinationCidrBlock'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['DestinationCidrBlock'] = net
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['TargetVpcSubnetId'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['Properties']['TargetVpcSubnetId'] = subnet
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['DependsOn'] = {}
                    config.fragment['Resources']['Cvpnerout' + netname + subname]['DependsOn'] = 'CvpneAss' + subname
                    config.fragment['Outputs']['Cvpnerout' + netname + subname] = {}
                    config.fragment['Outputs']['Cvpnerout' + netname + subname]['Description'] = 'Client VPN Endpoint Route' + net + subnet
                    config.fragment['Outputs']['Cvpnerout' + netname + subname]['Value'] = {'Ref': 'Cvpnerout' + netname + subname}
                    config.fragment['Outputs']['Cvpnerout' + netname + subname]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Cvpnerout' + netname + subname ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Cvpne Association Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def authrule(vpne,cidr,group,sub):
    # Network Association
    # Where:
    # vpne = ClientVpnEndpointId
    # sub = SubnetId
    # cidr = cidr list
    try:
        if ' ' in cidr:
            cidr = cidr.replace(' ','')
        if ',' in cidr:
            cidrlist = list(cidr.split(','))
        else:
            cidrlist = []
            cidrlist.append(cidr)
            for net in cidrlist:
                netname = net
                if ':' in netname:
                    netname = netname.replace(':','')
                if '-' in netname:
                    netname = netname.replace('-','')
                if '/' in netname:
                    netname = netname.replace('/','')
                if '.' in netname:
                    netname = netname.replace('.','')
                    config.fragment['Resources']['Cvpneauthrule' + netname] = {}
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Type'] = 'AWS::EC2::ClientVpnAuthorizationRule'
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties'] = {}
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['ClientVpnEndpointId'] = {}
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['ClientVpnEndpointId'] = { "Ref": vpne }
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['Description'] = {}
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['Description'] = 'Cvpne authrule' + net
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['TargetNetworkCidr'] = {}
                    config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['TargetNetworkCidr'] = net
                    if group != 'All':
                        config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['AccessGroupId'] = {}
                        config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['AccessGroupId'] = group
                    else:
                        config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['AuthorizeAllGroups'] = {}
                        config.fragment['Resources']['Cvpneauthrule' + netname]['Properties']['AuthorizeAllGroups'] = "True"
                    config.fragment['Resources']['Cvpneauthrule' + netname]['DependsOn'] = []
                    for subnet in sub:
                        subname = subnet
                        if ' ' in subname:
                            subname = subname.replace(' ','')
                        subname = subname.replace('-','')
                        config.fragment['Resources']['Cvpneauthrule' + netname]['DependsOn'].append('CvpneAss' + subname)
                    config.fragment['Outputs']['Cvpneauthrule' + netname] = {}
                    config.fragment['Outputs']['Cvpneauthrule' + netname]['Description'] = 'Client VPN Endpoint Route' + net + subnet
                    config.fragment['Outputs']['Cvpneauthrule' + netname]['Value'] = {'Ref': 'Cvpneauthrule' + netname}
                    config.fragment['Outputs']['Cvpneauthrule' + netname]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Cvpneauthrule' + netname ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Cvpne Association Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

