import config
def create(name,srvtk,dep,keylist):
    # Where:
    # name = Resource Name
    # srvtk = The service token to access the service, such as an Amazon SNS topic ARN or Lambda function ARN.
    # dep = dependence
    # keylist = multiple 
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::CloudFormation::CustomResource'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['ServiceToken'] = {}
        config.fragment['Resources'][name]['Properties']['ServiceToken'] = srvtk
        if keylist != '':
            for k,v in keylist.items():
                config.fragment['Resources'][name]['Properties'][k] = {}
                config.fragment['Resources'][name]['Properties'][k] = v
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = {}
        config.fragment['Outputs'][name]['Description'] = 'Custom Resource' + name
        config.fragment['Outputs'][name]['Value'] = {}
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        config.fragment['Outputs'][name]['Export'] = {}
        config.fragment['Outputs'][name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Custom Resource' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
