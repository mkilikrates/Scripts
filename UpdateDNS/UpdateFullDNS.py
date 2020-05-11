#!/usr/bin/python3.8
import logging
import traceback
import boto3
import json
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def main(argv):
    hostname = ''
    MPrivIP=''
    MPubIP=''
    MIPv6=''
    PubIPV6={}
    PrivIPV4={}
    PubIPV4={}
    hostedzones=''
    instanceid = str(sys.argv[1])
    region = str(sys.argv[2])
    detailtype = 'EC2 Instance State-change Notification'
    state = str(sys.argv[3])
    print ('Instance: {0}'.format(instanceid))
    print ('Region: {0}'.format(region))
    try:
        if detailtype == 'EC2 Instance State-change Notification': # if is state change notification from EC2
            print('Instance: {}'.format(instanceid))
            print('State: {}'.format(state))
            if state == 'running': # if notification is running to create/update DNS
                try:
                    client_ec2 = boto3.client('ec2',region_name=region) #describe instance to get all atributes
                    descinst = client_ec2.describe_instances(
                        InstanceIds=[
                            instanceid
                        ],
                        DryRun=False
                    )
                    for reservation in descinst['Reservations']:
                        for instance in reservation['Instances']:
                            MPrivIP=instance['PrivateIpAddress']
                            if 'PublicIpAddress' in instance:
                                MPubIP = instance['PublicIpAddress'] # get main public ipv4
                            if 'Tags' in instance:
                                for tag in instance['Tags']:
                                    if tag['Key'] == 'Name':
                                        hostname = tag['Value']  #get instance Name tag to use as hostname
                                    if tag['Key'] == 'HZ':
                                        hostedzones = tag['Value']  #get instance HZ tag to find the hosted zones this instance should be registered
                                        if ',' in hostedzones:
                                            hostedzones = hostedzones.split(', ')
                            eniid=0
                            for eni in instance['NetworkInterfaces']:
                                if 'Ipv6Addresses' in eni:
                                    ipv6id = 0
                                    PubIPV6[eniid] = {}
                                    for ipv6 in eni['Ipv6Addresses']:
                                        if eniid == 0:
                                            MIPv6 = ipv6['Ipv6Address']
                                            PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                        if eniid != 0:
                                            PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                        ipv6id=ipv6id+1
                                if 'PrivateIpAddresses' in eni:
                                    ipv4id = 0
                                    PrivIPV4[eniid] = {}
                                    for ipv4 in eni['PrivateIpAddresses']:
                                        PrivIPV4[eniid][ipv4id] = ipv4['PrivateIpAddress']
                                        if 'Association' in ipv4:
                                            PubIPV4[eniid] = ipv4['Association']['PublicIp']
                                        ipv4id=ipv4id+1
                                eniid=eniid+1
                    print(
                        'Instance : {0}\nHostname: {1}\nMainPrivateIpAddress: {2}\nMainPublic IPv4: {3}\nMainPublic IPv6: {4}\nSecPublic IPv6: {5}\nSecPrivate IPv4: {6}\nSecPublic IPv4: {7}\nHosted Zone IDs: {8}\n'.format(
                            instanceid, hostname, MPrivIP, MPubIP, MIPv6, PubIPV6, PrivIPV4, PubIPV4, hostedzones
                            )
                        )
                    if hostedzones !='':
                        for zoneid in hostedzones:
                            try:
                                client_r53 = boto3.client('route53')
                                zone = client_r53.get_hosted_zone(
                                    Id = zoneid
                                )
                                zonename=zone['HostedZone']['Name']
                                zonetype=zone['HostedZone']['Config']['PrivateZone']
                                if zonetype == True and hostname !='':
                                    print (
                                        'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PRIVATED ZONE'.format(
                                            zoneid, zonename
                                        )
                                    )
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'UPSERT',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'A',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MPrivIP
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )

                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PrivIPV4)):
                                        for ipid in range(len(PrivIPV4[intid])):
                                            ip=PrivIPV4[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'UPSERT',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'A',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'UPSERT',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'AAAA',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MIPv6
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV6)):
                                        for ipid in range(len(PubIPV6[intid])):
                                            ip=PubIPV6[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'UPSERT',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'AAAA',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                                if zonetype == False and hostname !='' and MPubIP !='':
                                    print (
                                        'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PUBLIC ZONE'.format(
                                            zoneid, zonename
                                        )
                                    )
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'UPSERT',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'A',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MPubIP
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV4)):
                                        ip=PubIPV4[intid]
                                        try:
                                            recset = client_r53.change_resource_record_sets(
                                                ChangeBatch={
                                                    'Comment': 'Intance :' + instanceid,
                                                    'Changes': [
                                                        {
                                                            'Action': 'UPSERT',
                                                            'ResourceRecordSet': {
                                                                'Name': hostname + '-' + str(intid) + '.' + zonename,
                                                                'Type': 'A',
                                                                'TTL': 300,
                                                                'ResourceRecords': [
                                                                    {
                                                                        'Value': ip
                                                                    },
                                                                ],
                                                            },
                                                        },
                                                    ],
                                                },
                                                HostedZoneId=zoneid,
                                            )
                                        except Exception as e:
                                            logger.error('ERROR: {}'.format(e))
                                            traceback.print_exc()
                                            response["statusCode"] = "500"
                                            response["body"] = str(e)
                                            return response
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'UPSERT',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'AAAA',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MIPv6
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV6)):
                                        for ipid in range(len(PubIPV6[intid])):
                                            ip=PubIPV6[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'UPSERT',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'AAAA',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                            except Exception as e:
                                logger.error('ERROR: {}'.format(e))
                                traceback.print_exc()
                                response["statusCode"] = "500"
                                response["body"] = str(e)
                                return response
                except Exception as e:
                    logger.error('ERROR: {}'.format(e))
                    traceback.print_exc()
                    response["statusCode"] = "500"
                    response["body"] = str(e)
                    return response
            if state == 'terminated' or 'stopped': # if notification is terminated to remove DNS
                try:
                    client_ec2 = boto3.client('ec2',region_name=region) #describe instance to get all atributes
                    descinst = client_ec2.describe_instances(
                        InstanceIds=[
                            instanceid
                        ],
                        DryRun=False
                    )
                    for reservation in descinst['Reservations']:
                        for instance in reservation['Instances']:
                            MPrivIP=instance['PrivateIpAddress']
                            if 'PublicIpAddress' in instance:
                                MPubIP = instance['PublicIpAddress'] # get main public ipv4
                            if 'Tags' in instance:
                                for tag in instance['Tags']:
                                    if tag['Key'] == 'Name':
                                        hostname = tag['Value']  #get instance Name tag to use as hostname
                                    if tag['Key'] == 'HZ':
                                        hostedzones = tag['Value']  #get instance HZ tag to find the hosted zones this instance should be registered
                                        if ',' in hostedzones:
                                            hostedzones = hostedzones.split(', ')
                            eniid=0
                            for eni in instance['NetworkInterfaces']:
                                if 'Ipv6Addresses' in eni:
                                    ipv6id = 0
                                    PubIPV6[eniid] = {}
                                    for ipv6 in eni['Ipv6Addresses']:
                                        if eniid == 0:
                                            MIPv6 = ipv6['Ipv6Address']
                                            PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                        if eniid != 0:
                                            PubIPV6[eniid][ipv6id] = ipv6['Ipv6Address']
                                        ipv6id=ipv6id+1
                                if 'PrivateIpAddresses' in eni:
                                    ipv4id = 0
                                    PrivIPV4[eniid] = {}
                                    for ipv4 in eni['PrivateIpAddresses']:
                                        PrivIPV4[eniid][ipv4id] = ipv4['PrivateIpAddress']
                                        if 'Association' in ipv4:
                                            PubIPV4[eniid] = ipv4['Association']['PublicIp']
                                        ipv4id=ipv4id+1
                                eniid=eniid+1
                    print(
                        'Instance : {0}\nHostname: {1}\nMainPrivateIpAddress: {2}\nMainPublic IPv4: {3}\nMainPublic IPv6: {4}\nSecPublic IPv6: {5}\nSecPrivate IPv4: {6}\nSecPublic IPv4: {7}\nHosted Zone IDs: {8}\n'.format(
                            instanceid, hostname, MPrivIP, MPubIP, MIPv6, PubIPV6, PrivIPV4, PubIPV4, hostedzones
                            )
                        )
                    if hostedzones !='':
                        for zoneid in hostedzones:
                            try:
                                client_r53 = boto3.client('route53')
                                zone = client_r53.get_hosted_zone(
                                    Id = zoneid
                                )
                                zonename=zone['HostedZone']['Name']
                                zonetype=zone['HostedZone']['Config']['PrivateZone']
                                if zonetype == True and hostname !='':
                                    print (
                                        'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PRIVATED ZONE'.format(
                                            zoneid, zonename
                                        )
                                    )
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'DELETE',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'A',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MPrivIP
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )

                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PrivIPV4)):
                                        for ipid in range(len(PrivIPV4[intid])):
                                            ip=PrivIPV4[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'DELETE',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'A',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'DELETE',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'AAAA',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MIPv6
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV6)):
                                        for ipid in range(len(PubIPV6[intid])):
                                            ip=PubIPV6[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'DELETE',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'AAAA',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                                if zonetype == False and hostname !='' and MPubIP !='':
                                    print (
                                        'Hosted Zone ID : {0}\nHosted Zone name : {1}\n IS PUBLIC ZONE'.format(
                                            zoneid, zonename
                                        )
                                    )
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'DELETE',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'A',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MPubIP
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV4)):
                                        ip=PubIPV4[intid]
                                        try:
                                            recset = client_r53.change_resource_record_sets(
                                                ChangeBatch={
                                                    'Comment': 'Intance :' + instanceid,
                                                    'Changes': [
                                                        {
                                                            'Action': 'DELETE',
                                                            'ResourceRecordSet': {
                                                                'Name': hostname + '-' + str(intid) + '.' + zonename,
                                                                'Type': 'A',
                                                                'TTL': 300,
                                                                'ResourceRecords': [
                                                                    {
                                                                        'Value': ip
                                                                    },
                                                                ],
                                                            },
                                                        },
                                                    ],
                                                },
                                                HostedZoneId=zoneid,
                                            )
                                        except Exception as e:
                                            logger.error('ERROR: {}'.format(e))
                                            traceback.print_exc()
                                            response["statusCode"] = "500"
                                            response["body"] = str(e)
                                            return response
                                    try:
                                        recset = client_r53.change_resource_record_sets(
                                            ChangeBatch={
                                                'Comment': 'Intance :' + instanceid,
                                                'Changes': [
                                                    {
                                                        'Action': 'DELETE',
                                                        'ResourceRecordSet': {
                                                            'Name': hostname + '.' + zonename,
                                                            'Type': 'AAAA',
                                                            'TTL': 300,
                                                            'ResourceRecords': [
                                                                {
                                                                    'Value': MIPv6
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                            HostedZoneId=zoneid,
                                        )
                                    except Exception as e:
                                        logger.error('ERROR: {}'.format(e))
                                        traceback.print_exc()
                                        response["statusCode"] = "500"
                                        response["body"] = str(e)
                                        return response
                                    for intid in range(len(PubIPV6)):
                                        for ipid in range(len(PubIPV6[intid])):
                                            ip=PubIPV6[intid][ipid]
                                            try:
                                                recset = client_r53.change_resource_record_sets(
                                                    ChangeBatch={
                                                        'Comment': 'Intance :' + instanceid,
                                                        'Changes': [
                                                            {
                                                                'Action': 'DELETE',
                                                                'ResourceRecordSet': {
                                                                    'Name': hostname + '-' + str(intid) + '-' + str(ipid) + '.' + zonename,
                                                                    'Type': 'AAAA',
                                                                    'TTL': 300,
                                                                    'ResourceRecords': [
                                                                        {
                                                                            'Value': ip
                                                                        },
                                                                    ],
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    HostedZoneId=zoneid,
                                                )
                                            except Exception as e:
                                                logger.error('ERROR: {}'.format(e))
                                                traceback.print_exc()
                                                response["statusCode"] = "500"
                                                response["body"] = str(e)
                                                return response
                            except Exception as e:
                                logger.error('ERROR: {}'.format(e))
                                traceback.print_exc()
                                response["statusCode"] = "500"
                                response["body"] = str(e)
                                return response
                except Exception as e:
                    logger.error('ERROR: {}'.format(e))
                    traceback.print_exc()
                    response["statusCode"] = "500"
                    response["body"] = str(e)
                    return response
        response = {}
        response["statusCode"] = "200"
        response["body"] = json.dumps('DNS Update Success!')
        return response
    except Exception as e:
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(sys.argv)
