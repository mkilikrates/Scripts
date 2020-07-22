import config
def main(name):
    try:
        config.fragment['Resources']['Vpc6'+ name] = {}
        config.fragment['Resources']['Vpc6'+ name]['Type'] = 'AWS::EC2::VPCCidrBlock'
        config.fragment['Resources']['Vpc6'+ name]['Properties'] = {}
        config.fragment['Resources']['Vpc6'+ name]['Properties']['AmazonProvidedIpv6CidrBlock'] = "true"
        config.fragment['Resources']['Vpc6'+ name]['Properties']['VpcId'] = {'Ref': 'Vpc' + name}
        config.fragment['Resources']['Vpc6'+ name]['DependsOn'] = {}
        config.fragment['Resources']['Vpc6'+ name]['DependsOn'] = 'Vpc' + name
        config.fragment['Outputs']['IPV6'+ name] = {}
        config.fragment['Outputs']['IPV6'+ name]['Description'] = 'VPC IPv6 Range'
        config.fragment['Outputs']['IPV6'+ name]['Value'] = { "Fn::Select": [ 0, { "Fn::GetAtt": [ 'Vpc' + name, "Ipv6CidrBlocks" ] } ] }
        config.fragment['Outputs']['IPV6'+ name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'IPV6'+ name ] ] } }
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


