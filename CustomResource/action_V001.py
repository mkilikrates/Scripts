import config
import ds

def main():
    try:
        #locals
        nslist = []
        dnslist = []
        directId = config.resproper['DirectoryId']
        action = ds.desc_ds(directId)
        config.logger.info('Action: {}'.format(action))
        for directory in action['DirectoryDescriptions']:
            dns = directory['DnsIpAddrs']
            for resolver in dns:
                if ':' in resolver:
                    resip,resport = resolver.split(':', 1)
                else:
                    resip = resolver
                    resport = "53"
                nslist.append({"Ip" : resip, "Port" : resport})
        action = {}
        action["statusCode"] = "200"
        action["Reason"] = ("Custom Resource found!")
        action["DnsIpAddrs"] = nslist
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
    return action