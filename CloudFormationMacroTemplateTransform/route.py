import config
def addv4(name,dst,RTname,gwtype,gw):
    # Where:
    # name = prefix name eg: PubDefaultIpv4 will generate PubDefaultIpv4IGW
    # dst = CIDR destination range
    # RTname = Route Table to add route
    # gwtype = Gateway type to add route (EgressOnlyInternetGatewayId/GatewayId/InstanceId/NatGatewayId/NetworkInterfaceId)
    # gw = Gateway Target
    try:
        config.fragment['Resources'][name + gw] = {}
        config.fragment['Resources'][name + gw]['Type'] = 'AWS::EC2::Route'
        config.fragment['Resources'][name + gw]['Properties'] = {}
        config.fragment['Resources'][name + gw]['Properties']['DestinationCidrBlock'] = {}
        config.fragment['Resources'][name + gw]['Properties']['DestinationCidrBlock'] = dst
        config.fragment['Resources'][name + gw]['Properties']['RouteTableId'] = {}
        config.fragment['Resources'][name + gw]['Properties']['RouteTableId']['Ref'] = RTname
        config.fragment['Resources'][name + gw]['Properties'][gwtype] = {}
        config.fragment['Resources'][name + gw]['Properties'][gwtype]['Ref'] = gw
        config.fragment['Resources'][name + gw]['DependsOn'] = []
        if gwtype == 'GatewayId':
            config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw + 'Attach' ]
        else:
            config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw ]
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route ' + name + gw + ' Add Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def addv6(name,dst,RTname,gwtype,gw):
    try:
        config.fragment['Resources'][name + gw] = {}
        config.fragment['Resources'][name + gw]['Type'] = 'AWS::EC2::Route'
        config.fragment['Resources'][name + gw]['Properties'] = {}
        config.fragment['Resources'][name + gw]['Properties']['DestinationIpv6CidrBlock'] = {}
        config.fragment['Resources'][name + gw]['Properties']['DestinationIpv6CidrBlock'] = dst
        config.fragment['Resources'][name + gw]['Properties']['RouteTableId'] = {}
        config.fragment['Resources'][name + gw]['Properties']['RouteTableId']['Ref'] = RTname
        config.fragment['Resources'][name + gw]['Properties'][gwtype] = {}
        config.fragment['Resources'][name + gw]['Properties'][gwtype]['Ref'] = gw
        config.fragment['Resources'][name + gw]['DependsOn'] = []
        if gwtype == 'GatewayId':
            config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw + 'Attach' ]
        else:
            config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw ]
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route Add Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def prop(name,rtids,vgw,dep):
    try:
        config.fragment['Resources']['RTPROP' + name] = {}
        config.fragment['Resources']['RTPROP' + name]['Type'] = 'AWS::EC2::VPNGatewayRoutePropagation'
        config.fragment['Resources']['RTPROP' + name]['Properties'] = {}
        config.fragment['Resources']['RTPROP' + name]['Properties']['RouteTableIds'] = []
        config.fragment['Resources']['RTPROP' + name]['Properties']['RouteTableIds'] = rtids
        config.fragment['Resources']['RTPROP' + name]['Properties']['VpnGatewayId'] = {}
        config.fragment['Resources']['RTPROP' + name]['Properties']['VpnGatewayId'] = vgw
        if dep != '':
            config.fragment['Resources']['RTPROP' + name]['DependsOn'] = {}
            config.fragment['Resources']['RTPROP' + name]['DependsOn'] = dep
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Route Table Propagation' + name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

