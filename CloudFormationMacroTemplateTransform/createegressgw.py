import config
def main(name):
    try:
        config.fragment['Resources']['EgressGW' + name] = {}
        config.fragment['Resources']['EgressGW' + name]['Type'] = 'AWS::EC2::EgressOnlyInternetGateway'
        config.fragment['Resources']['EgressGW' + name]['Properties'] = {}
        config.fragment['Resources']['EgressGW' + name]['Properties']['VpcId'] = {}
        config.fragment['Resources']['EgressGW' + name]['Properties']['VpcId']['Ref'] = 'Vpc' + name
        config.fragment['Resources']['EgressGW' + name]['DependsOn'] = {}
        config.fragment['Resources']['EgressGW' + name]['DependsOn'] = 'Vpc6' + name
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


