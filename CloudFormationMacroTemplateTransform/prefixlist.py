import config
def create(name,AddressFamily,DualStack):
    try:
        config.fragment['Resources']['RT' + name + vpcname] = {}
        config.fragment['Resources']['RT' + name + vpcname]['Type'] = 'AWS::EC2::RouteTable'
        config.fragment['Resources']['RT' + name + vpcname]['Properties'] = {}
        config.fragment['Resources']['RT' + name + vpcname]['Properties']['VpcId'] = {}
        config.fragment['Resources']['RT' + name + vpcname]['Properties']['VpcId']['Ref'] = 'Vpc' + vpcname
        config.fragment['Resources']['RT' + name + vpcname]['Properties']['Tags'] = {}
        config.fragment['Resources']['RT' + name + vpcname]['Properties']['Tags'] = [{'Key': 'Name', 'Value': name + vpcname}, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        config.fragment['Resources']['RT' + name + vpcname]['DependsOn'] = {}
        if DualStack == 'Yes':
            config.fragment['Resources']['RT' + name + vpcname]['DependsOn'] = 'Vpc6' + vpcname
        else:
            config.fragment['Resources']['RT' + name + vpcname]['DependsOn'] = 'Vpc' + vpcname
        config.fragment['Outputs']['RT' + name + vpcname] = {}
        config.fragment['Outputs']['RT' + name + vpcname]['Description'] = 'Route Table ID'
        config.fragment['Outputs']['RT' + name + vpcname]['Value'] = {'Ref': 'RT' + name + vpcname}
        config.fragment['Outputs']['RT' + name + vpcname]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'RT' + name + vpcname ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route Table RT' + name + vpcname + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response


