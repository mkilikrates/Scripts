import config
def main(name,rol,stack):
    # Where:
    # name = Name to be used on resource name (Name)
    # rol = Name to be used on resource name (Name)
    # stack = If needs to take care of dependency stack (Yes / No)
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::IAM::InstanceProfile'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['Path'] = {}
        config.fragment['Resources'][name]['Properties']['Path'] = "/"
        config.fragment['Resources'][name]['Properties']['Roles'] = []
        config.fragment['Resources'][name]['Properties']['Roles'] = [rol]
        if stack == 'yes':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = rol
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'Iam Instance Profile'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        config.fragment['Outputs'][name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Iam Instance profile Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

