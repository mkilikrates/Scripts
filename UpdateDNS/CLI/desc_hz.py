#!/usr/bin/python3.8
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
        logger.error('ERROR: {}'.format(e))
        traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

if __name__ == "__main__":
   main(sys.argv)
