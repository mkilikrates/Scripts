#!/usr/bin/python3.8
import config
def main(vpcId,region):
    try:
        client_ec2 = config.boto3.client('ec2',region_name=region) #describe instance to get all atributes
        descvpc = client_ec2.describe_vpcs(
            VpcIds=[
                vpcId
            ],
            DryRun=False
        )
        return descvpc
    except Exception as e:
        response = {}
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(sys.argv)
