import config
def main(vpcname,name,AZ):
    # Where:
    # name = prefix name eg: FE will get subnet resource FESubAZ1a
    # AZ = Availability zone
    try:
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]] = {}
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Type'] = 'AWS::EC2::EIP'
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Properties'] = {}
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Properties']['Domain'] = {}
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Properties']['Domain'] = 'Vpc' + vpcname
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Properties']['Tags'] = {}
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'NatEIPAZ' + vpcname + AZ[-2:] ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['DependsOn'] = {}
        config.fragment['Resources']['NatEIPAZ' + vpcname + AZ[-2:]]['DependsOn'] = 'Vpc' + vpcname
        config.fragment['Outputs']['NatEIPAZ' + vpcname + AZ[-2:]] = {}
        config.fragment['Outputs']['NatEIPAZ' + vpcname + AZ[-2:]]['Description'] = 'Elastic IP for Nat instance ID'
        config.fragment['Outputs']['NatEIPAZ' + vpcname + AZ[-2:]]['Value'] = {'Ref': 'NatEIPAZ' + vpcname + AZ[-2:]}
        config.fragment['Outputs']['NatEIPAZ' + vpcname + AZ[-2:]]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'NatEIPAZ' + vpcname + AZ[-2:] ] ] } }
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Type'] = 'AWS::EC2::NatGateway'
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties'] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['AllocationId'] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['AllocationId'] = { 'Fn::GetAtt' : ['NatEIPAZ' + vpcname + AZ[-2:], 'AllocationId']}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['SubnetId'] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['SubnetId']['Ref'] = vpcname + name + 'SubAZ' + AZ[-2:]
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['Tags'] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'NATgwAZ' + vpcname + AZ[-2:] ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['DependsOn'] = {}
        config.fragment['Resources']['NATgwAZ' + vpcname + AZ[-2:]]['DependsOn'] = 'NatEIPAZ' + vpcname + AZ[-2:]
        config.fragment['Outputs']['NATgwAZ' + vpcname + AZ[-2:]] = {}
        config.fragment['Outputs']['NATgwAZ' + vpcname + AZ[-2:]]['Description'] = 'Nat instance ID'
        config.fragment['Outputs']['NATgwAZ' + vpcname + AZ[-2:]]['Value'] = {'Ref': 'NATgwAZ' + vpcname + AZ[-2:]}
        config.fragment['Outputs']['NATgwAZ' + vpcname + AZ[-2:]]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'NATgwAZ' + vpcname + AZ[-2:] ] ] } }
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

