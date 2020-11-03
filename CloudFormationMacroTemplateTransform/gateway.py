import config
def igw(name,DualStack,dep):
    try:
        config.fragment['Resources']['IGW' + name] = {}
        config.fragment['Resources']['IGW' + name]['Type'] = 'AWS::EC2::InternetGateway'
        config.fragment['Resources']['IGW' + name]['Properties'] = {}
        config.fragment['Resources']['IGW' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['IGW' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'IGW' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['IGW' + name]['DependsOn'] = {}
            config.fragment['Resources']['IGW' + name]['DependsOn'] = dep
        config.fragment['Outputs']['IGW' + name] = {}
        config.fragment['Outputs']['IGW' + name]['Description'] = 'Internet Gateway ID'
        config.fragment['Outputs']['IGW' + name]['Value'] = {'Ref': 'IGW' + name}
        config.fragment['Outputs']['IGW' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'IGW' + name ] ] } }
        config.fragment['Resources']['IGW' + name + 'Attach'] = {}
        config.fragment['Resources']['IGW' + name + 'Attach']['Type'] = 'AWS::EC2::VPCGatewayAttachment'
        config.fragment['Resources']['IGW' + name + 'Attach']['Properties'] = {}
        config.fragment['Resources']['IGW' + name + 'Attach']['Properties']['VpcId'] = {}
        config.fragment['Resources']['IGW' + name + 'Attach']['Properties']['VpcId']['Ref'] = 'Vpc' + name
        config.fragment['Resources']['IGW' + name + 'Attach']['Properties']['InternetGatewayId'] = {}
        config.fragment['Resources']['IGW' + name + 'Attach']['Properties']['InternetGatewayId']['Ref'] = 'IGW' + name
        config.fragment['Resources']['IGW' + name + 'Attach']['DependsOn'] = {}
        config.fragment['Resources']['IGW' + name + 'Attach']['DependsOn'] = 'IGW' + name
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Internet Gateway IGW' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def vgw(name,asn,desc,vgtype,bgp,dep):
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::VPNGateway'
        config.fragment['Resources'][name]['Properties'] = {}
        if bgp == 1:
            config.fragment['Resources'][name]['Properties']['AmazonSideAsn'] = {}
            config.fragment['Resources'][name]['Properties']['AmazonSideAsn'] = asn
        config.fragment['Resources'][name]['Properties']['Type'] = {}
        config.fragment['Resources'][name]['Properties']['Type'] = vgtype
        config.fragment['Resources'][name]['Properties']['Tags'] = {}
        if desc !='':
            config.fragment['Resources'][name]['Properties']['Tags'] = [{'Key': 'Description', 'Value': desc}]
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'VGW ID'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VGW Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def tgw(name,asn,desc,bgp,autoacceptshrdattach,defrtassoc,defrtprop,dnssup,multicastsup,ecmpsup,dep):
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::TransitGateway'
        config.fragment['Resources'][name]['Properties'] = {}
        if bgp == 1:
            config.fragment['Resources'][name]['Properties']['AmazonSideAsn'] = {}
            config.fragment['Resources'][name]['Properties']['AmazonSideAsn'] = asn
        config.fragment['Resources'][name]['Properties']['AutoAcceptSharedAttachments'] = {}
        config.fragment['Resources'][name]['Properties']['AutoAcceptSharedAttachments'] = autoacceptshrdattach
        config.fragment['Resources'][name]['Properties']['DefaultRouteTableAssociation'] = {}
        config.fragment['Resources'][name]['Properties']['DefaultRouteTableAssociation'] = defrtassoc
        config.fragment['Resources'][name]['Properties']['DefaultRouteTablePropagation'] = {}
        config.fragment['Resources'][name]['Properties']['DefaultRouteTablePropagation'] = defrtprop
        config.fragment['Resources'][name]['Properties']['DnsSupport'] = {}
        config.fragment['Resources'][name]['Properties']['DnsSupport'] = dnssup
        config.fragment['Resources'][name]['Properties']['MulticastSupport'] = {}
        config.fragment['Resources'][name]['Properties']['MulticastSupport'] = multicastsup
        config.fragment['Resources'][name]['Properties']['VpnEcmpSupport'] = {}
        config.fragment['Resources'][name]['Properties']['VpnEcmpSupport'] = ecmpsup
        if desc !='':
            config.fragment['Resources'][name]['Properties']['Description'] = {}
            config.fragment['Resources'][name]['Properties']['Description'] = desc
        config.fragment['Resources'][name]['Properties']['Tags'] = {}
        config.fragment['Resources'][name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'TGW ID'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('TGW Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def eggw(name,dep):
    try:
        config.fragment['Resources']['EgressGW' + name] = {}
        config.fragment['Resources']['EgressGW' + name]['Type'] = 'AWS::EC2::EgressOnlyInternetGateway'
        config.fragment['Resources']['EgressGW' + name]['Properties'] = {}
        config.fragment['Resources']['EgressGW' + name]['Properties']['VpcId'] = {}
        config.fragment['Resources']['EgressGW' + name]['Properties']['VpcId']['Ref'] = 'Vpc' + name
        if dep != '':
            config.fragment['Resources']['EgressGW' + name]['DependsOn'] = {}
            config.fragment['Resources']['EgressGW' + name]['DependsOn'] = dep
        config.fragment['Outputs']['EgressGW' + name] = {}
        config.fragment['Outputs']['EgressGW' + name]['Description'] = 'IPv6 Egress Onlly Internet Gateway ID'
        config.fragment['Outputs']['EgressGW' + name]['Value'] = {'Ref': 'EgressGW' + name}
        config.fragment['Outputs']['EgressGW' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'EgressGW' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VPC IPv6 Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def cgw(name,asn,addr,vgtype,bgp,dep):
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::CustomerGateway'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['IpAddress'] = {}
        config.fragment['Resources'][name]['Properties']['IpAddress'] = addr
        config.fragment['Resources'][name]['Properties']['BgpAsn'] = {}
        if bgp == 1:
            config.fragment['Resources'][name]['Properties']['BgpAsn'] = asn
        else:
            config.fragment['Resources'][name]['Properties']['BgpAsn'] = 65000
        config.fragment['Resources'][name]['Properties']['Type'] = {}
        config.fragment['Resources'][name]['Properties']['Type'] = vgtype
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'CGW ID'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VGW Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def vpn(name,cgw,bgp,mygw,vgtype,dep):
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::VPNConnection'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['CustomerGatewayId'] = {}
        config.fragment['Resources'][name]['Properties']['CustomerGatewayId'] = cgw
        if bgp == 1:
            config.fragment['Resources'][name]['Properties']['StaticRoutesOnly'] = 'False'
        else:
            config.fragment['Resources'][name]['Properties']['StaticRoutesOnly'] = 'True'
        if vgtype == 'TGW':
            config.fragment['Resources'][name]['Properties']['TransitGatewayId'] = {}
            config.fragment['Resources'][name]['Properties']['TransitGatewayId'] = mygw
        if vgtype == 'VGW':
            config.fragment['Resources'][name]['Properties']['VpnGatewayId'] = {}
            config.fragment['Resources'][name]['Properties']['VpnGatewayId'] = mygw
        config.fragment['Resources'][name]['Properties']['Type'] = {}
        config.fragment['Resources'][name]['Properties']['Type'] = 'ipsec.1'
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'VPN ID'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VPN Connection Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def eip(vpcname,name,dep):
    # Where:
    # name = prefix name eg: FE will get subnet resource FESubAZ1a
    # AZ = Availability zone
    try:
        config.fragment['Resources']['EIP' + vpcname + name] = {}
        config.fragment['Resources']['EIP' + vpcname + name]['Type'] = 'AWS::EC2::EIP'
        config.fragment['Resources']['EIP' + vpcname + name]['Properties'] = {}
        config.fragment['Resources']['EIP' + vpcname + name]['Properties']['Domain'] = {}
        config.fragment['Resources']['EIP' + vpcname + name]['Properties']['Domain'] = 'Vpc' + vpcname
        config.fragment['Resources']['EIP' + vpcname + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['EIP' + vpcname + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'EIP' + vpcname + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['EIP' + vpcname + name]['DependsOn'] = {}
            config.fragment['Resources']['EIP' + vpcname + name]['DependsOn'] = dep
        config.fragment['Outputs']['EIP' + vpcname + name] = {}
        config.fragment['Outputs']['EIP' + vpcname + name]['Description'] = 'Elastic IP for ' + name
        config.fragment['Outputs']['EIP' + vpcname + name]['Value'] = {'Ref': 'EIP' + vpcname + name}
        config.fragment['Outputs']['EIP' + vpcname + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'EIP' + vpcname + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('EIP Allocation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def eipass(name,instid,enid,pvtip,allocid,dep):
    # Where:
    # name = prefix name eg: FE will get subnet resource FESubAZ1a
    # AZ = Availability zone
    try:
        config.fragment['Resources']['EIPASS' + name] = {}
        config.fragment['Resources']['EIPASS' + name]['Type'] = 'AWS::EC2::EIPAssociation'
        config.fragment['Resources']['EIPASS' + name]['Properties'] = {}
        config.fragment['Resources']['EIPASS' + name]['Properties']['AllocationId'] = {}
        config.fragment['Resources']['EIPASS' + name]['Properties']['AllocationId'] = allocid
        if instid != '':
            config.fragment['Resources']['EIPASS' + name]['Properties']['InstanceId'] = {}
            config.fragment['Resources']['EIPASS' + name]['Properties']['InstanceId'] = instid
        else:
            config.fragment['Resources']['EIPASS' + name]['Properties']['NetworkInterfaceId'] = {}
            config.fragment['Resources']['EIPASS' + name]['Properties']['NetworkInterfaceId'] = enid
            if pvtip != '':
                config.fragment['Resources']['EIPASS' + name]['Properties']['PrivateIpAddress'] = {}
                config.fragment['Resources']['EIPASS' + name]['Properties']['PrivateIpAddress'] = enid
        if dep != '':
            config.fragment['Resources']['EIPASS' + name]['DependsOn'] = {}
            config.fragment['Resources']['EIPASS' + name]['DependsOn'] = dep
        config.fragment['Outputs']['EIPASS' + name] = {}
        config.fragment['Outputs']['EIPASS' + name]['Description'] = 'Elastic IP for ' + name
        config.fragment['Outputs']['EIPASS' + name]['Value'] = {'Ref': 'EIPASS'  + name}
        config.fragment['Outputs']['EIPASS' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'EIPASS'  + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('EIP Allocation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def vgwattch(name,vgw,vpc):
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::VPCGatewayAttachment'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['VpcId'] = {}
        config.fragment['Resources'][name]['Properties']['VpcId'] = vpc
        config.fragment['Resources'][name]['Properties']['VpnGatewayId'] = {}
        config.fragment['Resources'][name]['Properties']['VpnGatewayId'] = vgw
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'VGW Attachment ID'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VGW Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response