#!/usr/bin/python3.8
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
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(sys.argv)
