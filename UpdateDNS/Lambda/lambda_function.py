import config
import desc_ec2
import desc_hz
import recordset_hz
import desc_vpc
import associatevpc_r53
import disassociatevpc_r53
import list_hz

def lambda_handler(event, context):
    config.logger.info('event: {}'.format(event))
    #config.logger.info('context: {}'.format(context))
    #config.logger.info (
    #    'EventDetail : {0}\n'.format(
    #        event['detail']
    #    )
    #)
    response = {}
    try:
        # Globals
        config.region = event['region']
        config.accountId = event['account']
        config.detailtype = event['detail-type']
        if config.detailtype == 'EC2 Instance State-change Notification':
            config.instanceid = event['detail']['instance-id']
            config.state = event['detail']['state']
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
                                if ',' in tag['Value']:
                                    config.hostedzones = list(tag['Value'].split(','))
                                else:
                                    config.hostedzones.append(tag['Value'])
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
                #config.logger.info(
                #'Instance : {0}\nHostname: {1}\nMainPrivateIpAddress: {2}\nMainPublic IPv4: {3}\nMainPublic IPv6: {4}\nSecPublic IPv6: {5}\nSecPrivate IPv4: {6}\nSecPublic IPv4: {7}\nHosted Zone IDs: {8}\n'.format(
                #    config.instanceid, config.hostname, config.MPrivIP, config.MPubIP, config.MIPv6, config.PubIPV6, config.PrivIPV4, config.PubIPV4, config.hostedzones
                #    )
                #)
            if config.state == 'running': # if notification is running to create/update DNS
                config.logger.info('Registering instance ID: {0}\n Name: {1}\nHosted Zone IDs: {2}'.format(config.instanceid,config.hostname,config.hostedzones))
                for zoneid in config.hostedzones:
                    hz = desc_hz.main(zoneid)
                    zonename=hz['HostedZone']['Name']
                    zoneprivate=hz['HostedZone']['Config']['PrivateZone']
                    config.logger.info('Registering instance ID: {0}\n Name: {1}\nHosted Zone Name: {2}'.format(config.instanceid,config.hostname,zonename))
                    if zoneprivate == True and config.hostname !='': #Main IPv[46]
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
            if config.state == 'shutting-down' or config.state == 'stopping': # if notification is terminated to remove DNS
                config.logger.info('Deregistering instance ID: {0}\n Name: {1}\nHosted Zone IDs: {2}'.format(config.instanceid,config.hostname,config.hostedzones))
                config.logger.info(len(config.hostedzones))
                for zoneid in config.hostedzones:
                    hz = desc_hz.main(zoneid)
                    zonename=hz['HostedZone']['Name']
                    zoneprivate=hz['HostedZone']['Config']['PrivateZone']
                    config.logger.info('Deregistering instance ID: {0}\n Name: {1}\nHosted Zone Name: {2}'.format(config.instanceid,config.hostname,zonename))
                    if zoneprivate == True and config.hostname !='': #Main IPv[46]
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
        if config.detailtype == 'AWS API Call via CloudTrail':
            config.eventName = event['detail']['eventName']
            if config.eventName == 'CreateTags': # if notification is Create tags in vpc resource to create/update DNS
                for resources in event['detail']['requestParameters']['resourcesSet']['items']:
                    resourceId = resources['resourceId']
                    if resourceId.startswith('vpc-'):
                        config.vpcId = resourceId
                        config.logger.info(
                            'Associating VPC id: {0}\n'.format(
                                config.vpcId
                                )
                            )
                        vpcs = desc_vpc.main(config.vpcId,config.region)
                        for vpc in vpcs['Vpcs']:
                            if 'Tags' in vpc:
                                for tag in vpc['Tags']:
                                    if tag['Key'] == 'HZ':
                                        if ',' in tag['Value']:
                                            config.hostedzones = list(tag['Value'].split(','))
                                        else:
                                            config.hostedzones.append(tag['Value'])
                                        for zoneid in config.hostedzones:
                                            hz = desc_hz.main(zoneid)
                                            zonename=hz['HostedZone']['Name']
                                            zoneprivate=hz['HostedZone']['Config']['PrivateZone']
                                            if zoneprivate == True:
                                                assocvpc = associatevpc_r53.main(zoneid,config.region,config.vpcId)
                    else:
                        response["statusCode"] = "200"
                        response["body"] = config.json.dumps('Nothing to do with Resource ID: ' + resourceId)
            if config.eventName == 'DeleteVpc': # if notification is running to create/update DNS
                config.vpcId = event['detail']['requestParameters']['vpcId']
                config.logger.info(
                    'Disassociating VPC id: {0}\n'.format(
                        config.vpcId
                        )
                    )
                lshz = list_hz.main()
                if 'HostedZones' in lshz:
                    for hostedzones in lshz['HostedZones']:
                        zoneid = ((hostedzones['Id']).replace('/hostedzone/', ''))
                        zonename = hostedzones['Name']
                        zoneprivate = hostedzones['Config']['PrivateZone']
                        if zoneprivate == True:
                            # try remove instead of verify first
                            disassocvpc = disassociatevpc_r53.main(zoneid,config.region,config.vpcId)
        if not 'statusCode' in response:
            response["statusCode"] = "200"
            response["body"] = config.json.dumps('DNS Update Success!')
        #json_formatted_response = config.json.dumps(response, indent=2)
        config.logger.info (response)
        return response
    except Exception as e:
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
