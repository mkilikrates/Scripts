import config
def desc_ds(directId):
    try:
        client_ds = config.boto3.client('ds', region_name=config.region)
        dns = client_ds.describe_directories(
            DirectoryIds=[
                directId,
            ]
        )
        return dns
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response
