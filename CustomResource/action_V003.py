import config
import ec2

def check_num(s):
  try:
    int(s)
    return True
  except:
    return False


def main():
    try:
        #locals
        region = config.region
        cgwid = config.resproper['VPNConn']['Customer-Gateway-Id']
        gwtype = config.resproper['VPNConn']['Gateway-Type']
        gwid = config.resproper['VPNConn']['Gateway-Id']
        tunnelopt = config.resproper['VPNConn']['VPNOptions']['TunnelOptions']
        tid = 0
        for tunnelid in tunnelopt:
            for k,v in tunnelid.items():        
                if isinstance(v,list):
                    itid = 0
                    for item in v:
                        if isinstance(item,dict):
                            for k1,v1 in item.items():
                                if check_num(v1) == True:
                                    v1 = int(v1)
                                    tunnelopt[tid][k][itid][k1] = int(v1)
                                if v1 == 'false':
                                    tunnelopt[tid][k][itid][k1] = False
                                if v1 == 'true':
                                    tunnelopt[tid][k][itid][k1] = True
                        elif isinstance(v,list):
                            it1id = 0
                            for item1 in v:
                                if isinstance(item1,dict):
                                    for k2,v2 in item1.items():
                                        if check_num(v2) == True:
                                            v2 = int(v2)
                                            tunnelopt[tid][k][itid][k1][it1id][k2] = int(v2)
                                        if v2 == 'false':
                                            tunnelopt[tid][k][itid][k1][it1id][k2] = False
                                        if v2 == 'true':
                                            tunnelopt[tid][k][itid][k1][it1id][k2] = True
                                it1id = it1id + 1
                        itid = itid + 1
                elif isinstance(v,dict):
                    for k1,v1 in item.items():
                        if check_num(v1) == True:
                            v1 = int(v1)
                            tunnelopt[tid][k][itid][k1] = int(v1)
                        if v1 == 'false':
                            tunnelopt[tid][k][itid][k1] = False
                        if v1 == 'true':
                            tunnelopt[tid][k][itid][k1] = True
                else:
                    if check_num(v) == True:
                        v = int(v)
                        tunnelopt[tid][k] = int(v)
                    if v == 'false':
                        tunnelopt[tid][k] = False
                    if v == 'true':
                        tunnelopt[tid][k] = True
            tid = tid + 1
        vpnopts = config.resproper['VPNConn']['VPNOptions']
        for k,v in vpnopts.items():        
            if v == 'false':
                vpnopts[k] = False
            if v == 'true':
                vpnopts[k] = True
        response = {}
        response['VPNConn'] = {}
        if config.reqtype == 'Create':
            if gwtype == 'VGW':
                keylist = {}
                keylist['CustomerGatewayId'] = {}
                keylist['CustomerGatewayId'] = cgwid
                keylist['Type'] = {}
                keylist['Type'] = 'ipsec.1'
                keylist['VpnGatewayId'] = {}
                keylist['VpnGatewayId'] = gwid
                keylist['Options'] = {}
                keylist['Options'] = vpnopts
            elif gwtype == 'TGW':
                keylist = {}
                keylist = {}
                keylist['CustomerGatewayId'] = {}
                keylist['CustomerGatewayId'] = cgwid
                keylist['Type'] = {}
                keylist['Type'] = 'ipsec.1'
                keylist['TransitGatewayId'] = {}
                keylist['TransitGatewayId'] = gwid
                keylist['Options'] = {}
                keylist['Options'] = vpnopts
            action = ec2.create_vpn_connection(region,keylist)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = action["VpnConnection"]["VpnConnectionId"]
            action["VPNConn"] = {}
            action["VPNConn"]["VpnConnectionId"] = {}
            action["VPNConn"]["VpnConnectionId"] = action["VpnConnection"]["VpnConnectionId"]
        elif config.reqtype == 'Delete':
            vpnid = config.phyresId
            action = ec2.delete_vpn_connection(region,vpnid)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = 'None'
            action["VPNConn"] = {}
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
            action["Reason"] = ("Nothing to do here!")
        response['Reason'] = action['Reason']
        response['PhysicalResourceId'] = action['PhysicalResourceId']
        response['VPNConn'] = action['VPNConn']
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response