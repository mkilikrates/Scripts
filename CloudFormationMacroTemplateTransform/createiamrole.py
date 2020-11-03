import config
def manag(name,srv,pol):
    # Where:
    # name = Name to be used on resource name ('IAMRole' + Hostname')
    # srv = AWS Service name to use this role (eg: ec2.amazonaws.com)
    # pol = Managed Policy arn to be attached to this role
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::IAM::Role'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['Description'] = {}
        config.fragment['Resources'][name]['Properties']['Description'] = 'Service ' + srv + 'using managed policy: ' + pol
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Version'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Version'] = "2012-10-17"
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = "Allow"
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = { "Service": [ srv ] }
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = []
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = [ "sts:AssumeRole" ]
        config.fragment['Resources'][name]['Properties']['Path'] = {}
        config.fragment['Resources'][name]['Properties']['Path'] = "/"
        config.fragment['Resources'][name]['Properties']['ManagedPolicyArns'] = []
        config.fragment['Resources'][name]['Properties']['ManagedPolicyArns'] = [ pol ]
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'Iam Role'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        config.fragment['Outputs'][name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Iam Role Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def pol(name,srv,pol,dep):
    # Where:
    # name = Name to be used on resource name ('IAMRole' + Hostname')
    # srv = AWS Service name to use this role (eg: ec2.amazonaws.com)
    # pol = Managed Policy arn to be attached to this role
    try:
        config.fragment['Resources'][name] = {}
        config.fragment['Resources'][name]['Type'] = 'AWS::IAM::Role'
        config.fragment['Resources'][name]['Properties'] = {}
        config.fragment['Resources'][name]['Properties']['Description'] = {}
        config.fragment['Resources'][name]['Properties']['Description'] = 'Service ' + srv + 'using policy '
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Version'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Version'] = "2012-10-17"
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = "Allow"
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = {}
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = { "Service": [ srv ] }
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = []
        config.fragment['Resources'][name]['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = [ "sts:AssumeRole" ]
        config.fragment['Resources'][name]['Properties']['Path'] = {}
        config.fragment['Resources'][name]['Properties']['Path'] = "/"
        config.fragment['Resources'][name]['Properties']['Policies'] = []
        config.fragment['Resources'][name]['Properties']['Policies'] = [ pol ]
        if dep != '':
            config.fragment['Resources'][name]['DependsOn'] = {}
            config.fragment['Resources'][name]['DependsOn'] = dep
        config.fragment['Outputs'][name] = {}
        config.fragment['Outputs'][name]['Description'] = 'Iam Role'
        config.fragment['Outputs'][name]['Value'] = {'Ref': name}
        config.fragment['Outputs'][name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Iam Role Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

