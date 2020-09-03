import config
def main(VPC,name):
    try:
        config.fragment['Resources']['SecG' + name] = {}
        config.fragment['Resources']['SecG' + name]['Type'] = 'AWS::EC2::SecurityGroup'
        config.fragment['Resources']['SecG' + name]['Properties'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupName'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupName'] = 'SecG' + name
        config.fragment['Resources']['SecG' + name]['Properties']['GroupDescription'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['GroupDescription'] = 'SecG' + name + '-' + VPC
        config.fragment['Resources']['SecG' + name]['Properties']['VpcId'] = {}
        config.fragment['Resources']['SecG' + name]['Properties']['VpcId'] = VPC
        config.fragment['Outputs']['SecG' + name] = {}
        config.fragment['Outputs']['SecG' + name]['Description'] = 'Security Group ID' + name + '-' + VPC
        config.fragment['Outputs']['SecG' + name]['Value'] = {'Ref': 'SecG' + name}
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


