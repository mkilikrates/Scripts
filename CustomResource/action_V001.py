import config
import ds

def main():
    try:
        #locals
        nslist = []
        directId = config.resproper['DirectoryId']
        action = .ds.desc_ds(directId)
        config.logger.info('Response: {}'.format(action))
        for directory in action['DirectoryDescriptions']:
            dns = directory['DnsIpAddrs']
            if ' ' in dns:
                dns = dns.replace(' ', '')
            if ',' in dns:
                dnslist = list(dns.split(','))
            else:
                dnslist.append(dns)
            for resolver in dnslist:
                if ':' in resolver:
                    resip,resport = resolver.split(':', 1)
                else:
                    resip = resolver
                    resport = 53
                nslist.append({ "Ip" : resip, "Port" : resport })
        action = {}
        action["statusCode"] = "200"
        action["Reason"] = config.json.dumps('Custom Resource found!')
        action["DnsIpAddrs"] = nslist
        config.logger.info('Response: {}'.format(action))
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["Reason"] = str(e)
        config.logger.info('Response: {}'.format(action))
    return action