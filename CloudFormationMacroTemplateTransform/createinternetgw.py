import config
def main(name,DualStack):
    try:
        config.fragment['Resources']['IGW' + name] = {}
        config.fragment['Resources']['IGW' + name]['Type'] = 'AWS::EC2::InternetGateway'
        config.fragment['Resources']['IGW' + name]['Properties'] = {}
        config.fragment['Resources']['IGW' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['IGW' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'IGW' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        config.fragment['Resources']['IGW' + name]['DependsOn'] = {}
        if DualStack == 'Yes':
            config.fragment['Resources']['IGW' + name]['DependsOn'] = 'Vpc6' + name
        else:
            config.fragment['Resources']['IGW' + name]['DependsOn'] = 'Vpc' + name
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


