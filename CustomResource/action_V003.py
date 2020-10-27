import config
import ec2

def main():
    try:
        #locals
        region = config.region
        cgwid = config.resproper['VPNConn']['Customer-Gateway-Id']
        gwtype = config.resproper['VPNConn']['Gateway-Type']
        gwid = config.resproper['VPNConn']['Gateway-Id']
        vpnopts = config.resproper['VPNConn']['VPNOptions']
        response = {}
        response['VPNConn'] = {}
        if config.reqtype == 'Create':
            if gwtype == 'VGW':
                keylist = {}
                keylist['data'] = {}
                keylist['data']['CustomerGatewayId'] = {}
                keylist['data']['CustomerGatewayId'] = cgwid
                keylist['data']['Type'] = {}
                keylist['data']['Type'] = 'ipsec.1'
                keylist['data']['VpnGatewayId'] = {}
                keylist['data']['VpnGatewayId'] = gwid
                keylist['data']['Options'] = {}
                keylist['data']['Options'] = vpnopts
            elif gwtype == 'TGW':
                keylist = {}
                keylist['data'] = {}
                keylist['data']['TransitGatewayId'] = {}
                keylist['data']['TransitGatewayId'] = cgwid
                keylist['data']['Type'] = {}
                keylist['data']['Type'] = 'ipsec.1'
                keylist['data']['VpnGatewayId'] = {}
                keylist['data']['VpnGatewayId'] = gwid
                keylist['data']['Options'] = {}
                keylist['data']['Options'] = vpnopts
            action = ec2.create_vpn_connection(region,keylist)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = action["VpnConnection"]["VpnConnectionId"]
        elif config.reqtype == 'Delete':
            vpnid = config.phyresId
            action = ec2.delete_vpn_connection(region,vpnid)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = 'None'
        else:
            config.logger.info('Action: Nothing to do here! - {}'.format(config.reqtype))
            action["Reason"] = ("Nothing to do here!")
        response['VpnConnection'] = action['VpnConnection']
        response['Reason'] = action['Reason']
        response['PhysicalResourceId'] = action['PhysicalResourceId']
        action = {}
        action["statusCode"] = "200"
        action['Reason'] = {}
        action["Reason"] = response['Reason']
        action['PhysicalResourceId'] = response['PhysicalResourceId']
        action["VpnConnection"] = {}
        action["VpnConnection"] = response['VpnConnection']
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
    return action