import config
def create(name,instprop,dep):
    # Where:
    # name = Name to be used on resource name (LT + Name)
    # instprop = Instance Properties
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::EC2::Instance'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties'] = instprop
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'Instance Template' + name
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        config.fragment['Outputs'][name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Instance ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

