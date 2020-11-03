import config
def main(vpcname,name,SubCidr,AZ,DualStack,PUbORV6,IPV6id,RT):
    # Where:
    # vpcname = name used on vpc (where stack creates multiple vpcs)
    # name = prefix name eg: FE will generate FESubAZ1a
    # SubCidr = Ipv4 subnet Cidr
    # AZ = Availability Zone
    # DualStack = Yes for use IPv6 from Amazon
    # PUbORV6 = (Pub,IPv6,None) to enable MapPublicIpOnLaunch or AssignIpv6AddressOnCreation or None
    # IPV6id = id to be used on ipv6 cidr creation
    # RT = Route table to be associated with subnet
    try:
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Type'] = 'AWS::EC2::Subnet'
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties'] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['VpcId'] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['VpcId']['Ref'] = 'Vpc' + vpcname
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['AvailabilityZone'] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['AvailabilityZone'] = AZ
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['CidrBlock'] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['CidrBlock'] = SubCidr
        if PUbORV6 == 'None':
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['MapPublicIpOnLaunch'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['MapPublicIpOnLaunch'] = 'false'
        if PUbORV6 == 'Pub':
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['MapPublicIpOnLaunch'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['MapPublicIpOnLaunch'] = 'true'
        if PUbORV6 == 'IPv6' and DualStack == 'Yes':
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['AssignIpv6AddressOnCreation'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['AssignIpv6AddressOnCreation'] = 'true'
        if DualStack == 'Yes':
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['Ipv6CidrBlock'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['Ipv6CidrBlock'] = { "Fn::Select" : [ IPV6id, { "Fn::Cidr" : [ { "Fn::Select": [ 0, { "Fn::GetAtt": [ 'Vpc' + vpcname, "Ipv6CidrBlocks" ] } ] }, 256, 64 ] } ] }
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['DependsOn'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['DependsOn'] = 'Vpc6' + vpcname
        else:
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['DependsOn'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['DependsOn'] = 'Vpc' + vpcname
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['Tags'] = {}
        config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:]]['Properties']['Tags'] = [{'Key': 'Name', 'Value': name + AZ[-2:]}, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:]] = {}
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:]]['Description'] = 'Subnet  ID'
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:]]['Value'] = {'Ref': vpcname + name + 'SubAZ' + AZ[-2:]}
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:]]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name + 'SubAZ' + AZ[-2:] ] ] } }
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'CIDR'] = {}
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'CIDR']['Description'] = 'Subnet  IPv4 CIDR'
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'CIDR']['Value'] = SubCidr
        config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'CIDR']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name + 'SubAZ' + AZ[-2:] + 'CIDR' ] ] } }
        if DualStack == 'Yes':
            config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'IPv6'] = {}
            config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'IPv6']['Description'] = 'Subnet  IPv6 CIDR'
            config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'IPv6']['Value'] = { "Fn::Select" : [ IPV6id, { "Fn::Cidr" : [ { "Fn::Select": [ 0, { "Fn::GetAtt": [ 'Vpc' + vpcname, "Ipv6CidrBlocks" ] } ] }, 256, 64 ] } ] }
            config.fragment['Outputs'][vpcname + name + 'SubAZ' + AZ[-2:] + 'IPv6']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name + 'SubAZ' + AZ[-2:] + 'IPv6' ] ] } }
        # Create Public RT Association
        if RT != 'None':
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Type'] = 'AWS::EC2::SubnetRouteTableAssociation'
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Properties'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Properties']['RouteTableId'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Properties']['RouteTableId']['Ref'] = RT
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Properties']['SubnetId'] = {}
            config.fragment['Resources'][vpcname + name + 'SubAZ' + AZ[-2:] + 'RtAssoc']['Properties']['SubnetId']['Ref'] = vpcname + name + 'SubAZ' + AZ[-2:]
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

def static(vpcname,name,SubCidr,AZ,DualStack,PUbORV6,SubCidrV6,RT,dep):
    # Where:
    # vpcname = name used on vpc (where stack creates multiple vpcs)
    # name = prefix name eg: FE will generate FESubAZ1a
    # SubCidr = Ipv4 subnet Cidr
    # AZ = Availability Zone
    # DualStack = Yes for use IPv6 from Amazon
    # PUbORV6 = (Pub,IPv6,None) to enable MapPublicIpOnLaunch or AssignIpv6AddressOnCreation or None
    # IPV6id = id to be used on ipv6 cidr creation
    # RT = Route table to be associated with subnet
    try:
        config.fragment['Resources'][vpcname + name] = {}
        config.fragment['Resources'][vpcname + name]['Type'] = 'AWS::EC2::Subnet'
        config.fragment['Resources'][vpcname + name]['Properties'] = {}
        config.fragment['Resources'][vpcname + name]['Properties']['VpcId'] = {}
        config.fragment['Resources'][vpcname + name]['Properties']['VpcId']['Ref'] = 'Vpc' + vpcname
        config.fragment['Resources'][vpcname + name]['Properties']['AvailabilityZone'] = {}
        config.fragment['Resources'][vpcname + name]['Properties']['AvailabilityZone'] = AZ
        config.fragment['Resources'][vpcname + name]['Properties']['CidrBlock'] = {}
        config.fragment['Resources'][vpcname + name]['Properties']['CidrBlock'] = SubCidr
        if PUbORV6 == 'None':
            config.fragment['Resources'][vpcname + name]['Properties']['MapPublicIpOnLaunch'] = {}
            config.fragment['Resources'][vpcname + name]['Properties']['MapPublicIpOnLaunch'] = 'false'
        if PUbORV6 == 'Pub':
            config.fragment['Resources'][vpcname + name]['Properties']['MapPublicIpOnLaunch'] = {}
            config.fragment['Resources'][vpcname + name]['Properties']['MapPublicIpOnLaunch'] = 'true'
        if PUbORV6 == 'IPv6' and DualStack == 'Yes':
            config.fragment['Resources'][vpcname + name]['Properties']['AssignIpv6AddressOnCreation'] = {}
            config.fragment['Resources'][vpcname + name]['Properties']['AssignIpv6AddressOnCreation'] = 'true'
        if DualStack == 'Yes':
            config.fragment['Resources'][vpcname + name]['Properties']['Ipv6CidrBlock'] = {}
            config.fragment['Resources'][vpcname + name]['Properties']['Ipv6CidrBlock'] = SubCidrV6
        config.fragment['Resources'][vpcname + name]['Properties']['Tags'] = {}
        config.fragment['Resources'][vpcname + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': name}, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources'][vpcname + name]['DependsOn'] = {}
            config.fragment['Resources'][vpcname + name]['DependsOn'] = dep
        config.fragment['Outputs'][vpcname + name] = {}
        config.fragment['Outputs'][vpcname + name]['Description'] = 'Subnet  ID'
        config.fragment['Outputs'][vpcname + name]['Value'] = {'Ref': vpcname + name}
        config.fragment['Outputs'][vpcname + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name ] ] } }
        config.fragment['Outputs'][vpcname + name + 'CIDR'] = {}
        config.fragment['Outputs'][vpcname + name + 'CIDR']['Description'] = 'Subnet  IPv4 CIDR'
        config.fragment['Outputs'][vpcname + name + 'CIDR']['Value'] = SubCidr
        config.fragment['Outputs'][vpcname + name + 'CIDR']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name + 'CIDR' ] ] } }
        if DualStack == 'Yes':
            config.fragment['Outputs'][vpcname + name + 'IPv6'] = {}
            config.fragment['Outputs'][vpcname + name + 'IPv6']['Description'] = 'Subnet  IPv6 CIDR'
            config.fragment['Outputs'][vpcname + name + 'IPv6']['Value'] = { "Fn::Select" : [ IPV6id, { "Fn::Cidr" : [ { "Fn::Select": [ 0, { "Fn::GetAtt": [ 'Vpc' + vpcname, "Ipv6CidrBlocks" ] } ] }, 256, 64 ] } ] }
            config.fragment['Outputs'][vpcname + name + 'IPv6']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" }, vpcname + name + 'IPv6' ] ] } }
        # Create Public RT Association
        if RT != 'None':
            config.fragment['Resources'][vpcname + name + 'RtAssoc'] = {}
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Type'] = 'AWS::EC2::SubnetRouteTableAssociation'
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Properties'] = {}
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Properties']['RouteTableId'] = {}
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Properties']['RouteTableId']['Ref'] = RT
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Properties']['SubnetId'] = {}
            config.fragment['Resources'][vpcname + name + 'RtAssoc']['Properties']['SubnetId']['Ref'] = vpcname + name
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

