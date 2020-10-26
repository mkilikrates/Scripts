import config
import ec2

def main():
    try:
        #locals
        region = config.region
        cgwid = config.resproper['CGCustomer-Gateway-IdWASN']
        gwtype = config.resproper['Gateway-Type']
        gwid = config.resproper['Gateway-Id']
        vpnopts = config.resproper['VPNOptions']
        response = {}
        response['VPNConn'] = {}
        response['Reason'] = {}
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
                keylist['TransitGatewayId'] = {}
                keylist['TransitGatewayId'] = cgwid
                keylist['Type'] = {}
                keylist['Type'] = 'ipsec.1'
                keylist['VpnGatewayId'] = {}
                keylist['VpnGatewayId'] = gwid
                keylist['Options'] = {}
                keylist['Options'] = vpnopts
            action = ec2.create_vpn_connection(region,keylist)
            config.logger.info('Action: {}'.format(action))
            action["Reason"] = ("Custom Resource created!")
            action["PhysicalResourceId"] = action["VpnConnection"]["VpnConnectionId"]
        elif config.reqtype == 'Delete':
            vpnid = config.phyresId
            action = ec2.delete_vpn_connection(region,vpnid)
            config.logger.info('Action: {}'.format(action))
            action["PhysicalResourceId"] = 'None'
            action["Reason"] = ("Custom Resource removed!")
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