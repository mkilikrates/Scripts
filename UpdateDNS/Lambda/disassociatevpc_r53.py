import config
def main(zoneid,region,vpcId):
    try:
        client_r53 = config.boto3.client('route53')
        disassociatevpc = client_r53.disassociate_vpc_from_hosted_zone(
            HostedZoneId=zoneid,
            VPC={
                'VPCRegion': region,
                'VPCId': vpcId
            },
            Comment='VPC ID: ' + vpcId + 'Region: ' + region,
        )
        return disassociatevpc
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
