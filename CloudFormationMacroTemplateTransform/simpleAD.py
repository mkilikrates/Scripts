import config
def create(recname,name,alias,desc,sso,pwd,netb,size,sub,vpc,dep):
    # Where:
    # name = Full Qualified Name for the directory. Pattern: ^([a-zA-Z0-9]+[\\.-])+([a-zA-Z0-9])+$
    # alias = (true | false). alias is used to construct the access URL for the directory, such as http://<alias>.awsapps.com
    # desc = Description for the directory. Maximum: 128 Pattern: ^([a-zA-Z0-9_])[\\a-zA-Z0-9_@#%*+=:?./!\s-]*$
    # sso = (true | false).Whether to enable single sign-on for a directory
    # pwd = The password for the directory administrator. Pattern: (?=^.{8,64}$)((?=.*\d)(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[^A-Za-z0-9\s])(?=.*[a-z])|(?=.*[^A-Za-z0-9\s])(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[A-Z])(?=.*[^A-Za-z0-9\s]))^.*
    # netb = NetBIOS name of the directory. Pattern: ^[^\\/:*?"<>|.]+[^\\/:*?"<>|]*$
    # size = (Large | Small). The size of the directory
    # sub = subnet list 
    # vpc = vpc id
    # dep = dependence
    try:
        config.fragment['Resources']['SimpleAD' + recname] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Type'] = 'AWS::DirectoryService::SimpleAD'
        config.fragment['Resources']['SimpleAD' + recname]['Properties'] = {}
        if alias != '':
            config.fragment['Resources']['SimpleAD' + recname]['Properties']['CreateAlias'] = {}
            config.fragment['Resources']['SimpleAD' + recname]['Properties']['CreateAlias'] = alias
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Description'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Description'] = desc
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['EnableSso'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['EnableSso'] = sso
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Name'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Name'] = name
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Password'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Password'] = pwd
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['ShortName'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['ShortName'] = netb
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Size'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['Size'] = size
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['VpcSettings'] = {}
        config.fragment['Resources']['SimpleAD' + recname]['Properties']['VpcSettings'] = { "SubnetIds" :  sub , "VpcId" : vpc }
        if dep != '':
            config.fragment['Resources']['SimpleAD' + recname]['DependsOn'] = {}
            config.fragment['Resources']['SimpleAD' + recname]['DependsOn'] = dep
        config.fragment['Outputs']['SimpleAD' + recname] = {}
        config.fragment['Outputs']['SimpleAD' + recname]['Description'] = 'Simple AD ID'
        config.fragment['Outputs']['SimpleAD' + recname]['Value'] = {'Ref': 'SimpleAD' + recname}
        config.fragment['Outputs']['SimpleAD' + recname]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'SimpleAD' + recname ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Simple AD ' + recname + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

