import config
def main():
    try:
        client_r53 = config.boto3.client('route53')
        lszone = client_r53.list_hosted_zones(
            MaxItems='100'
        )
        return lszone
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
