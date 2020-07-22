import config
def main(name,VpcCidr,UpdateDNS,PrivHZ):
    try:
        config.fragment['Resources']['Vpc' + name] = {}
        config.fragment['Resources']['Vpc' + name]['Type'] = 'AWS::EC2::VPC'
        config.fragment['Resources']['Vpc' + name]['Properties'] = {}
        config.fragment['Resources']['Vpc' + name]['Properties']['CidrBlock'] = VpcCidr
        config.fragment['Resources']['Vpc' + name]['Properties']['EnableDnsSupport'] = "true"
        config.fragment['Resources']['Vpc' + name]['Properties']['EnableDnsHostnames'] = "true"
        config.fragment['Resources']['Vpc' + name]['Properties']['InstanceTenancy'] = "default"
        config.fragment['Resources']['Vpc' + name]['Properties']['Tags'] = {}
        if UpdateDNS == 'Yes':
            if name == '':
                config.fragment['Resources']['Vpc' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {'Ref': 'AWS::StackName'}}, {'Key': 'HZ', 'Value': PrivHZ}]
            else:
                config.fragment['Resources']['Vpc' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': name}, {'Key': 'HZ', 'Value': PrivHZ}]
        else:
            if name == '':
                config.fragment['Resources']['Vpc' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {'Ref': 'AWS::StackName'}}]
            else:
                config.fragment['Resources']['Vpc' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': name}]
        config.fragment['Outputs']['Vpc' + name + 'ID'] = {}
        config.fragment['Outputs']['Vpc' + name + 'ID']['Description'] = 'VPC ID'
        config.fragment['Outputs']['Vpc' + name + 'ID']['Value'] = {'Ref': 'Vpc' + name}
        config.fragment['Outputs']['Vpc' + name + 'ID']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Vpc' + name + 'ID' ] ] } }
        config.fragment['Outputs']['Vpc' + name + 'CIDR'] = {}
        config.fragment['Outputs']['Vpc' + name + 'CIDR']['Description'] = 'VPC IPv4 CIDR'
        config.fragment['Outputs']['Vpc' + name + 'CIDR']['Value'] = VpcCidr
        config.fragment['Outputs']['Vpc' + name + 'CIDR']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Vpc' + name + 'CIDR' ] ] } }
        config.fragment['Outputs']['Vpc' + name + 'DefNACL'] = {}
        config.fragment['Outputs']['Vpc' + name + 'DefNACL']['Description'] = 'The Default ACL'
        config.fragment['Outputs']['Vpc' + name + 'DefNACL']['Value'] = { "Fn::GetAtt": [ 'Vpc' + name, "DefaultNetworkAcl" ] }
        config.fragment['Outputs']['Vpc' + name + 'DefNACL']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Vpc' + name + 'DefNACL' ] ] } }
        config.fragment['Outputs']['Vpc' + name + 'DefSG'] = {}
        config.fragment['Outputs']['Vpc' + name + 'DefSG']['Description'] = 'The Default Security Group'
        config.fragment['Outputs']['Vpc' + name + 'DefSG']['Value'] = { "Fn::GetAtt": [ 'Vpc' + name, "DefaultSecurityGroup" ] }
        config.fragment['Outputs']['Vpc' + name + 'DefSG']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'Vpc' + name + 'DefSG' ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VPC Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response



