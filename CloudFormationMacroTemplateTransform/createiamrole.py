import config
def manag(name,srv,act,pol):
    # Where:
    # name = Name to be used on resource name (Name + 'Role')
    # srv = AWS Service name to use this role (eg: ec2.amazonaws.com)
    # stack = If needs to take care of dependency stack (Yes / No)
    # pol = Managed Policy arn to be attached to this role
    try:
        config.fragment['Resources'][name + 'Role'] = {}
        config.fragment['Resources'][name + 'Role']['Type'] = 'AWS::IAM::Role'
        config.fragment['Resources'][name + 'Role']['Properties'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['Description'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['Description'] = 'Service ' + srv + 'using managed policy: ' + pol
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Version'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Version'] = "2012-10-17"
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement'] = []
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Effect'] = "Allow"
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Principal'] = { "Service": [ srv ] }
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = []
        config.fragment['Resources'][name + 'Role']['Properties']['AssumeRolePolicyDocument']['Statement']['Action'] = [ "sts:AssumeRole" ]
        config.fragment['Resources'][name + 'Role']['Properties']['Path'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['Path'] = "/"
        config.fragment['Resources'][name + 'Role']['Properties']['ManagedPolicyArns'] = {}
        config.fragment['Resources'][name + 'Role']['Properties']['ManagedPolicyArns'] = pol
        config.fragment['Outputs'][name + 'Role'] = {}
        config.fragment['Outputs'][name + 'Role']['Description'] = 'Iam Role'
        config.fragment['Outputs'][name + 'Role']['Value'] = {'Ref': name + 'Role'}
        config.fragment['Outputs'][name + 'Role']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , name + 'Role' ] ] } }
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

