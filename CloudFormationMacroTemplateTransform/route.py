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
        config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw + 'Attach' ]
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
        config.fragment['Resources'][name + gw]['DependsOn'] = [ RTname, gw + 'Attach' ]
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


