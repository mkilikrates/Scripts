import config
def createendpoint(name,direc,sg,sub,dep):
    try:
        config.fragment['Resources']['R53ResEnd' + name] = {}
        config.fragment['Resources']['R53ResEnd' + name]['Type'] = 'AWS::Route53Resolver::ResolverEndpoint'
        config.fragment['Resources']['R53ResEnd' + name]['Properties'] = {}
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Name'] = {}
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Name'] = name
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Direction'] = {}
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Direction'] = direc
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['IpAddresses'] = []
        for subnet in sub:    
            config.fragment['Resources']['R53ResEnd' + name]['Properties']['IpAddresses'].append( { "SubnetId" : subnet })
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['SecurityGroupIds'] = []
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['SecurityGroupIds'] = sg
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['R53ResEnd' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'R53ResEnd' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['R53ResEnd' + name]['DependsOn'] = {}
            config.fragment['Resources']['R53ResEnd' + name]['DependsOn'] = dep
        config.fragment['Outputs']['R53ResEnd' + name] = {}
        config.fragment['Outputs']['R53ResEnd' + name]['Description'] = {}
        config.fragment['Outputs']['R53ResEnd' + name]['Description'] = 'Resolver Endpoint ' + direc + ' ' + name
        config.fragment['Outputs']['R53ResEnd' + name]['Value'] = {}
        config.fragment['Outputs']['R53ResEnd' + name]['Value'] = {'Ref': 'R53ResEnd' + name}
        config.fragment['Outputs']['R53ResEnd' + name]['Export'] = {}
        config.fragment['Outputs']['R53ResEnd' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'R53ResEnd' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route53 Resolver Endpoint ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def createrule(name,domain,res,rulet,ip,dep):
    try:
        config.fragment['Resources']['R53ResRule' + name] = {}
        config.fragment['Resources']['R53ResRule' + name]['Type'] = 'AWS::Route53Resolver::ResolverRule'
        config.fragment['Resources']['R53ResRule' + name]['Properties'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['Name'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['Name'] = name
        config.fragment['Resources']['R53ResRule' + name]['Properties']['DomainName'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['DomainName'] = domain
        config.fragment['Resources']['R53ResRule' + name]['Properties']['ResolverEndpointId'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['ResolverEndpointId'] = res
        config.fragment['Resources']['R53ResRule' + name]['Properties']['RuleType'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['RuleType'] = rulet
        if rulet == 'FORWARD':    
            config.fragment['Resources']['R53ResRule' + name]['Properties']['TargetIps'] = []
            config.fragment['Resources']['R53ResRule' + name]['Properties']['TargetIps'] = ip
        config.fragment['Resources']['R53ResRule' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['R53ResRule' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'R53ResRule' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['R53ResRule' + name]['DependsOn'] = {}
            config.fragment['Resources']['R53ResRule' + name]['DependsOn'] = dep
        config.fragment['Outputs']['R53ResRule' + name] = {}
        config.fragment['Outputs']['R53ResRule' + name]['Description'] = {}
        config.fragment['Outputs']['R53ResRule' + name]['Description'] = 'Resolver Endpoint ' + rulet + ' ' + name
        config.fragment['Outputs']['R53ResRule' + name]['Value'] = {}
        config.fragment['Outputs']['R53ResRule' + name]['Value'] = {'Ref': 'R53ResRule' + name}
        config.fragment['Outputs']['R53ResRule' + name]['Export'] = {}
        config.fragment['Outputs']['R53ResRule' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'R53ResRule' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route53 Resolver rule ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def assocrule(name,ruleid,vpc,dep):
    try:
        config.fragment['Resources']['R53RRuleAss' + name] = {}
        config.fragment['Resources']['R53RRuleAss' + name]['Type'] = 'AWS::Route53Resolver::ResolverRuleAssociation'
        config.fragment['Resources']['R53RRuleAss' + name]['Properties'] = {}
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['Name'] = {}
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['Name'] = name
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['ResolverRuleId'] = {}
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['ResolverRuleId'] = ruleid
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['VPCId'] = {}
        config.fragment['Resources']['R53RRuleAss' + name]['Properties']['VPCId'] = vpc
        if dep != '':
            config.fragment['Resources']['R53RRuleAss' + name]['DependsOn'] = {}
            config.fragment['Resources']['R53RRuleAss' + name]['DependsOn'] = dep
        config.fragment['Outputs']['R53RRuleAss' + name] = {}
        config.fragment['Outputs']['R53RRuleAss' + name]['Description'] = {}
        config.fragment['Outputs']['R53RRuleAss' + name]['Description'] = 'Res Endpoint Assoc ' + name
        config.fragment['Outputs']['R53RRuleAss' + name]['Value'] = {}
        config.fragment['Outputs']['R53RRuleAss' + name]['Value'] = {'Ref': 'R53RRuleAss' + name}
        config.fragment['Outputs']['R53RRuleAss' + name]['Export'] = {}
        config.fragment['Outputs']['R53RRuleAss' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'R53RRuleAss' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route53 Resolver rule Association ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
