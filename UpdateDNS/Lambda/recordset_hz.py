import config
def main(action,rectype,ttl,zoneid,zonename,instanceid,hostname,IP):
    try:
        client_r53 = config.boto3.client('route53')
        recset = client_r53.change_resource_record_sets(
            ChangeBatch={
                'Comment': 'Intance :' + instanceid,
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': hostname + '.' + zonename,
                            'Type': rectype,
                            'TTL': ttl,
                            'ResourceRecords': [
                                {
                                    'Value': IP
                                },
                            ],
                        },
                    },
                ],
            },
            HostedZoneId=zoneid,
        )
        return recset
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
