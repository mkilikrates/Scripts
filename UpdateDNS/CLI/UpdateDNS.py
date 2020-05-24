#!/usr/bin/python3.8
import config
import desc_ec2
import desc_hz
import recordset_hz

def main(argv):
    try:
        config.instanceid = str(config.sys.argv[1])
        config.region = str(config.sys.argv[2])
        config.detailtype = 'EC2 Instance State-change Notification'
        config.state = str(config.sys.argv[3])
        print ('Instance: {0}'.format(config.instanceid))
        print ('Region: {0}'.format(config.region))
        print('Type: {}'.format(config.detailtype))
        if config.detailtype == 'EC2 Instance State-change Notification': # if is state change notification from EC2
            print('State: {}'.format(config.state))
            ec2 = desc_ec2.main(config.instanceid,config.region)
            for reservation in ec2['Reservations']:
                for instance in reservation['Instances']:
                    config.MPrivIP=instance['PrivateIpAddress']
                    if 'PublicIpAddress' in instance:
                        config.MPubIP = instance['PublicIpAddress'] # get main public ipv4
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                config.hostname = tag['Value']  #get instance Name tag to use as hostname
                            if tag['Key'] == 'HZ':
                                config.hostedzones = tag['Value']  #get instance HZ tag to find the hosted zones this instance should be registered
                                if ',' in config.hostedzones:
                                    config.hostedzones = config.hostedzones.strip()
                                    config.hostedzones = config.hostedzones.split(',')
                    eniid=0
                    for eni in instance['NetworkInterfaces']:
                        if 'Ipv6Addresses' in eni:
                            ipv6id = 0
                            config.PubIPV6[eniid] = {}
                            for ipv6 in eni['Ipv6Addresses']:
                                if eniid == 0:
                                    config.MIPv6 = ipv6['Ipv6Address']
                                    config.PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                if eniid != 0:
                                    config.PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                ipv6id=ipv6id+1
                        if 'PrivateIpAddresses' in eni:
                            ipv4id = 0
                            config.PrivIPV4[eniid] = {}
                            for ipv4 in eni['PrivateIpAddresses']:
                                config.PrivIPV4[eniid][ipv4id] = ipv4['PrivateIpAddress']
                                if 'Association' in ipv4:
                                    config.PubIPV4[eniid] = ipv4['Association']['PublicIp']
                                ipv4id=ipv4id+1
                        eniid=eniid+1
            print(
                'Instance : {0}\nHostname: {1}\nMainPrivateIpAddress: {2}\nMainPublic IPv4: {3}\nMainPublic IPv6: {4}\nSecPublic IPv6: {5}\nSecPrivate IPv4: {6}\nSecPublic IPv4: {7}\nHosted Zone IDs: {8}\n'.format(
                    config.instanceid, config.hostname, config.MPrivIP, config.MPubIP, config.MIPv6, config.PubIPV6, config.PrivIPV4, config.PubIPV4, config.hostedzones
                    )
                )
            if config.state == 'running': # if notification is running to create/update DNS
                print('Registering instance\n')
                if config.hostedzones !='':
                    for zoneid in config.hostedzones:
                        hz = desc_hz.main(zoneid)
                        zonename=hz['HostedZone']['Name']
                        zoneprivate=hz['HostedZone']['Config']['PrivateZone']
                        if zoneprivate == True and config.hostname !='': #Main IPv[46]
                            print (
                                'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PRIVATED ZONE'.format(
                                    zoneid, zonename
                                )
                            )
                            r53set = recordset_hz.main('UPSERT','A',300,zoneid,zonename,config.instanceid,config.hostname,config.MPrivIP)
                            if config.MIPv6 != '':
                                r53set = recordset_hz.main('UPSERT','AAAA',300,zoneid,zonename,config.instanceid,config.hostname,config.MIPv6)
                            for intid in range(len(config.PrivIPV4)): #Interface and additional IPv4
                                for ipid in range(len(config.PrivIPV4[intid])):
                                    ip=config.PrivIPV4[intid][ipid]
                                r53set = recordset_hz.main('UPSERT','A',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
                            if config.MIPv6 != '':
                                for intid in range(len(config.PubIPV6)):
                                    for ipid in range(len(config.PubIPV6[intid])):
                                        ip=config.PubIPV6[intid][ipid]
                                    r53set = recordset_hz.main('UPSERT','AAAA',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
                        if zoneprivate == False and config.hostname !='' and config.MPubIP !='':
                            print (
                                'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PUBLIC ZONE'.format(
                                    zoneid, zonename
                                )
                            )
                            r53set = recordset_hz.main('UPSERT','A',300,zoneid,zonename,config.instanceid,config.hostname,config.MPubIP)
                            if config.MIPv6 != '':
                                r53set = recordset_hz.main('UPSERT','AAAA',300,zoneid,zonename,config.instanceid,config.hostname,config.MIPv6)
                            for intid in range(len(config.PubIPV4)):
                                ip=config.PubIPV4[intid]
                                r53set = recordset_hz.main('UPSERT','A',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid),ip)
                            if config.MIPv6 != '':
                                for intid in range(len(config.PubIPV6)):
                                    for ipid in range(len(config.PubIPV6[intid])):
                                        ip=config.PubIPV6[intid][ipid]
                                    r53set = recordset_hz.main('UPSERT','AAAA',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
            if config.state == 'terminated' or config.state == 'stopped': # if notification is terminated to remove DNS
                print('Deregistering instance\n')
                if config.hostedzones !='':
                    for zoneid in config.hostedzones:
                        hz = desc_hz.main(zoneid)
                        zonename=hz['HostedZone']['Name']
                        zoneprivate=hz['HostedZone']['Config']['PrivateZone']
                        if zoneprivate == True and config.hostname !='': #Main IPv[46]
                            print (
                                'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PRIVATED ZONE'.format(
                                    zoneid, zonename
                                )
                            )
                            r53set = recordset_hz.main('DELETE','A',300,zoneid,zonename,config.instanceid,config.hostname,config.MPrivIP)
                            if config.MIPv6 != '':
                                r53set = recordset_hz.main('DELETE','AAAA',300,zoneid,zonename,config.instanceid,config.hostname,config.MIPv6)
                            for intid in range(len(config.PrivIPV4)): #Interface and additional IPv4
                                for ipid in range(len(config.PrivIPV4[intid])):
                                    ip=config.PrivIPV4[intid][ipid]
                                r53set = recordset_hz.main('DELETE','A',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
                            if config.MIPv6 != '':
                                for intid in range(len(config.PubIPV6)):
                                    for ipid in range(len(config.PubIPV6[intid])):
                                        ip=config.PubIPV6[intid][ipid]
                                    r53set = recordset_hz.main('DELETE','AAAA',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
                        if zoneprivate == False and config.hostname !='' and config.MPubIP !='':
                            print (
                                'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PUBLIC ZONE'.format(
                                    zoneid, zonename
                                )
                            )
                            r53set = recordset_hz.main('DELETE','A',300,zoneid,zonename,config.instanceid,config.hostname,config.MPubIP)
                            if config.MIPv6 != '':
                                r53set = recordset_hz.main('DELETE','AAAA',300,zoneid,zonename,config.instanceid,config.hostname,config.MIPv6)
                            for intid in range(len(config.PubIPV4)):
                                ip=config.PubIPV4[intid]
                                r53set = recordset_hz.main('DELETE','A',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid),ip)
                            if config.MIPv6 != '':
                                for intid in range(len(config.PubIPV6)):
                                    for ipid in range(len(config.PubIPV6[intid])):
                                        ip=config.PubIPV6[intid][ipid]
                                    r53set = recordset_hz.main('DELETE','AAAA',300,zoneid,zonename,config.instanceid,config.hostname + '-' + str(intid) + '-' + str(ipid),ip)
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('DNS Update Success!')
        json_formatted_response = config.json.dumps(response, indent=2)
        print (json_formatted_response)
        return response
    except Exception as e:
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(config.sys.argv)
