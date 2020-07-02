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
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
