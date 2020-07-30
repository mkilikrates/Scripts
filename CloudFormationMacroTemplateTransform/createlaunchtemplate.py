import config
def main(Name,InstType,AmiId,SecurityGroup,instprof,key):
    # Where:
    # Name = Name to be used on resource name (LT + Name)
    # InstType = InstanceType
    # AmiId = AMI to be used
    # SecurityGroup = SecurityGroup List
    # instprof = Instance profile
    try:
        config.fragment['Resources']['LT' + Name] = {}
        config.fragment['Resources']['LT' + Name]['Type'] = 'AWS::EC2::LaunchTemplate'
        config.fragment['Resources']['LT' + Name]['Properties'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateName'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateName'] = 'LT' + Name
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['DisableApiTermination'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['DisableApiTermination'] = 'false'
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceInitiatedShutdownBehavior'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceInitiatedShutdownBehavior'] = 'terminate'
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['ImageId'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['ImageId'] = AmiId
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceType'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceType'] = InstType
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['SecurityGroupIds'] = []
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['SecurityGroupIds'] = SecurityGroup
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['KeyName'] = []
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['KeyName'] = SecurityGroup
        if instprof !='':
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['IamInstanceProfile'] = []
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['IamInstanceProfile'] = instprof
        config.fragment['Outputs']['LT' + Name] = {}
        config.fragment['Outputs']['LT' + Name]['Description'] = 'Instance Template' + Name
        config.fragment['Outputs']['LT' + Name]['Value'] = {'Ref': 'LT' + Name}
        config.fragment['Outputs']['LT' + Name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'LT' + Name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Launch Template RT' + Name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

