import config
def main(zoneid):
    try:
        client_r53 = config.boto3.client('route53')
        zone = client_r53.get_hosted_zone(
            Id = zoneid
            )
        return zone
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response
