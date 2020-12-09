import config
def lb(name,DualStack,lbtype,sub,schem,sg,dep):
    # Where:
    # name = Name to be used on resource name ('LBV2' + name)
    # DualStack = The IP address type (dualstack | ipv4)
    # lbtype = The type of load balancer (application | gateway | network)
    # sub = subnet list ids 
    # schem = If load balancer is public or private (internal | internet-facing) You cannot specify a scheme for a Gateway Load Balancer
    try:
        config.fragment['Resources']['LBV2' + name] = {}
        config.fragment['Resources']['LBV2' + name]['Type'] = 'AWS::ElasticLoadBalancingV2::LoadBalancer'
        config.fragment['Resources']['LBV2' + name]['Properties'] = {}
        config.fragment['Resources']['LBV2' + name]['Properties']['Name'] = {}
        config.fragment['Resources']['LBV2' + name]['Properties']['Name'] = name
        config.fragment['Resources']['LBV2' + name]['Properties']['Type'] = {}
        config.fragment['Resources']['LBV2' + name]['Properties']['Type'] = lbtype
        config.fragment['Resources']['LBV2' + name]['Properties']['SubnetMappings'] = {}
        config.fragment['Resources']['LBV2' + name]['Properties']['SubnetMappings'] = sub
        if lbtype != 'gateway':
            config.fragment['Resources']['LBV2' + name]['Properties']['Scheme'] = {}
            config.fragment['Resources']['LBV2' + name]['Properties']['Scheme'] = schem
        if lbtype == 'application':
            config.fragment['Resources']['LBV2' + name]['Properties']['SecurityGroups'] = {}
            config.fragment['Resources']['LBV2' + name]['Properties']['SecurityGroups'] = sg
        config.fragment['Resources']['LBV2' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['LBV2' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'LBV2' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['LBV2' + name]['DependsOn'] = {}
            config.fragment['Resources']['LBV2' + name]['DependsOn'] = dep
        config.fragment['Outputs']['LBV2' + name] = {}
        config.fragment['Outputs']['LBV2' + name]['Description'] = 'Load Balancer ' + lbtype
        config.fragment['Outputs']['LBV2' + name]['Value'] = {'Ref': 'LBV2' + name}
        config.fragment['Outputs']['LBV2' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'LBV2' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Elastic Load Balancer ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def tgrp(name,vpc,tgrptype,proto,port,hcproto,hcport,hcpath,hcmatch,hcheltc,hcunheltc,hctout,hcintv,hctgatt,hctarg,dep):
    # Where:
    # name = Name to be used on resource name ('TGRP' + name)
    # proto = The protocol to use for routing traffic to the targets (GENEVE | HTTP | HTTPS | TCP | TCP_UDP | TLS | UDP)
    # tgrptype = The type of target that you must specify when registering targets with this target group (instance | ip | lambda)
    # port = The port on which the targets receive traffic (1-65536) 
    # hcproto = The protocol the load balancer uses when performing health checks on targets (GENEVE | HTTP | HTTPS | TCP | TCP_UDP | TLS | UDP)
    # hcport = The port the load balancer uses when performing health checks on targets (string)
    # hcmatch = Specifies the HTTP codes that healthy targets must use when responding to an HTTP health check. 
    # hcheltc = The number of consecutive health checks successes required before considering an unhealthy target healthy
    # hcunheltc = The number of consecutive health check failures required before considering a target unhealthy
    # hctout = The amount of time, in seconds, during which no response from a target means a failed health check (2-120)
    # hcintv = The approximate amount of time, in seconds, between health checks of an individual target
    # hctgatt = Specifies a target group attribute
    # hctarg = Specifies a target to add to a target group
    try:
        config.fragment['Resources']['TGRP' + name] = {}
        config.fragment['Resources']['TGRP' + name]['Type'] = 'AWS::ElasticLoadBalancingV2::TargetGroup'
        config.fragment['Resources']['TGRP' + name]['Properties'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Name'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Name'] = name
        config.fragment['Resources']['TGRP' + name]['Properties']['TargetType'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['TargetType'] = tgrptype
        config.fragment['Resources']['TGRP' + name]['Properties']['Protocol'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Protocol'] = proto
        config.fragment['Resources']['TGRP' + name]['Properties']['Port'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Port'] = port
        config.fragment['Resources']['TGRP' + name]['Properties']['Protocol'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Protocol'] = proto
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckEnabled'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckEnabled'] = True
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckProtocol'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckProtocol'] = hcproto
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthyThresholdCount'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckPort'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckPort'] = hcport
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthyThresholdCount'] = hcheltc
        config.fragment['Resources']['TGRP' + name]['Properties']['UnhealthyThresholdCount'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['UnhealthyThresholdCount'] = hcunheltc
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckTimeoutSeconds'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckTimeoutSeconds'] = hctout
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckIntervalSeconds'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckIntervalSeconds'] = hcintv
        if hcproto == 'HTTP' or hcproto == 'HTTPS':
            config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckPath'] = {}
            config.fragment['Resources']['TGRP' + name]['Properties']['HealthCheckPath'] = hcpath
            config.fragment['Resources']['TGRP' + name]['Properties']['Matcher'] = {}
            config.fragment['Resources']['TGRP' + name]['Properties']['Matcher'] = hcmatch
        if tgrptype != 'lambda':
            config.fragment['Resources']['TGRP' + name]['Properties']['VpcId'] = {}
            config.fragment['Resources']['TGRP' + name]['Properties']['VpcId'] = vpc
        if hctgatt != '':
            config.fragment['Resources']['TGRP' + name]['Properties']['TargetGroupAttributes'] = []
            config.fragment['Resources']['TGRP' + name]['Properties']['TargetGroupAttributes'] = hctgatt
        if hctarg != '':
            config.fragment['Resources']['TGRP' + name]['Properties']['Targets'] = []
            config.fragment['Resources']['TGRP' + name]['Properties']['Targets'] = hctarg
        config.fragment['Resources']['TGRP' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['TGRP' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'TGRP' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['TGRP' + name]['DependsOn'] = {}
            config.fragment['Resources']['TGRP' + name]['DependsOn'] = dep
        config.fragment['Outputs']['TGRP' + name] = {}
        config.fragment['Outputs']['TGRP' + name]['Description'] = 'Internet Gateway ID'
        config.fragment['Outputs']['TGRP' + name]['Value'] = {'Ref': 'TGRP' + name}
        config.fragment['Outputs']['TGRP' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'TGRP' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Target Group ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def lst(name,alpnpol,cert,act,lb,port,proto,sslpol,dep):
    # Where:
    # name = Name to be used on resource name ('LBV2LSTN' + name)
    # alpnpol = The name of the Application-Layer Protocol Negotiation (ALPN) policy
    # cert = The default SSL server certificate for a secure listener.
    # act = The actions for the default rule. 
    # lb = The Amazon Resource Name (ARN) of the load balancer
    # port = The port on which the load balancer is listening.(1-65535)
    # proto = The protocol for connections from clients to the load balancer. (GENEVE | HTTP | HTTPS | TCP | TCP_UDP | TLS | UDP)
    # sslpol = The security policy that defines which protocols and ciphers are supported
    # dep = dependecies before launch this resource
    try:
        config.fragment['Resources']['LBV2LSTN' + name] = {}
        config.fragment['Resources']['LBV2LSTN' + name]['Type'] = 'AWS::ElasticLoadBalancingV2::Listener'
        config.fragment['Resources']['LBV2LSTN' + name]['Properties'] = {}
        if alpnpol != '':
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['AlpnPolicy'] = []
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['AlpnPolicy'] = alpnpol
        if cert != '':
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Certificates'] = []
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Certificates'] = cert
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['DefaultActions'] = []
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['DefaultActions'] = act
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['LoadBalancerArn'] = {}
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['LoadBalancerArn'] = lb
        if port != '':
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Port'] = {}
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Port'] = port
        if proto == '':
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Protocol'] = {}
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Protocol'] = proto
        if sslpol == '':
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['SslPolicy'] = {}
            config.fragment['Resources']['LBV2LSTN' + name]['Properties']['SslPolicy'] = sslpol
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Tags'] = {}
        config.fragment['Resources']['LBV2LSTN' + name]['Properties']['Tags'] = [{'Key': 'Name', 'Value': {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'LBV2LSTN' + name ] ] } }, {'Key': 'StackName', 'Value': {'Ref': 'AWS::StackName'}}]
        if dep != '':
            config.fragment['Resources']['LBV2LSTN' + name]['DependsOn'] = {}
            config.fragment['Resources']['LBV2LSTN' + name]['DependsOn'] = dep
        config.fragment['Outputs']['LBV2LSTN' + name] = {}
        config.fragment['Outputs']['LBV2LSTN' + name]['Description'] = 'Load Balancer ' + lbtype
        config.fragment['Outputs']['LBV2LSTN' + name]['Value'] = {'Ref': 'LBV2LSTN' + name}
        config.fragment['Outputs']['LBV2LSTN' + name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'LBV2LSTN' + name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Elastic Load Balancer Listener ' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

