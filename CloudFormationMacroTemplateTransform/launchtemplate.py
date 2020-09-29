import config
import base64
def create(Name,InstType,AmiId,SecurityGroup,instprof,key,usrdata,PublicIP,dep):
    # Where:
    # Name = Name to be used on resource name (LT + Name)
    # InstType = InstanceType
    # AmiId = AMI to be used
    # SecurityGroup = SecurityGroup List
    # instprof = Instance profile
    # key = KeyName
    # usrdata = user data to automate deploy on instance
    # PublicIP = if request public 
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
        if PublicIP == 'Yes':
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['NetworkInterfaces'] = []
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['NetworkInterfaces'] = [ { 'AssociatePublicIpAddress' : 'true', 'DeviceIndex' : 0, 'Groups' : SecurityGroup } ]
        else:
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['NetworkInterfaces'] = [ { 'AssociatePublicIpAddress' : 'false', 'DeviceIndex' : 0, 'Groups' : SecurityGroup } ]
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['ImageId'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['ImageId'] = AmiId
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceType'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['InstanceType'] = InstType
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['KeyName'] = []
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['KeyName'] = key
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['Monitoring'] = {}
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['Monitoring'] = { 'Enabled' : 'false' }
        if instprof !='':
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['IamInstanceProfile'] = {}
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['IamInstanceProfile'] = { 'Name' : instprof }
        if usrdata !='None':
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['UserData'] = {}
            data = open(usrdata + ".cfg", "r").read()
            encoded = base64.b64encode(data.encode("utf-8"))
            config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['UserData'] = encoded
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['TagSpecifications'] = []
        config.fragment['Resources']['LT' + Name]['Properties']['LaunchTemplateData']['TagSpecifications'] = [ { 'ResourceType' : 'instance', 'Tags' : [ {'Key': 'Name', 'Value': { 'Ref': 'AWS::StackName' } } ] } ]
        if dep != '':
            config.fragment['Resources']['LT' + Name]['DependsOn'] = {}
            config.fragment['Resources']['LT' + Name]['DependsOn'] = dep
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

