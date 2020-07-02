import config
def main(instanceid,region):
    try:
        client_ec2 = config.boto3.client('ec2',region_name=region) #describe instance to get all atributes
        descinst = client_ec2.describe_instances(
            InstanceIds=[
                instanceid
            ],
            DryRun=False
        )
        return descinst
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
