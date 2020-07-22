import config
def main(VPC,name):
    try:
        config.fragment['Resources']['SG' + name] = {}
        config.fragment['Resources']['SG' + name]['Type'] = 'AWS::EC2::SecurityGroup'
        config.fragment['Resources']['SG' + name]['Properties'] = {}
        config.fragment['Resources']['SG' + name]['Properties']['GroupName'] = {}
        config.fragment['Resources']['SG' + name]['Properties']['GroupName'] = 'SG' + name
        config.fragment['Resources']['SG' + name]['Properties']['GroupDescription'] = {}
        config.fragment['Resources']['SG' + name]['Properties']['GroupDescription'] = 'SG' + name + '-' + VPC
        config.fragment['Resources']['SG' + name]['Properties']['VpcId'] = {}
        config.fragment['Resources']['SG' + name]['Properties']['VpcId'] = VPC
        config.fragment['Outputs']['SG' + name] = {}
        config.fragment['Outputs']['SG' + name]['Description'] = 'Security Group ID' + name + '-' + VPC
        config.fragment['Outputs']['SG' + name]['Value'] = {'Ref': 'SG' + name}
        config.fragment['Outputs']['SG' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'SG' + name ] ] } }
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



