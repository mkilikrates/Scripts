#!/usr/bin/python3.8
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
        print (recset)
        return recset
    except Exception as e:
        response = {}
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(sys.argv)
