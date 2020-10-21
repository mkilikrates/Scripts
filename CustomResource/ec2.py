import config
def allocate_address(region,domain):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        address = client_ec2.allocate_address(
            Domain=domain
        )
        return address
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def describe_addresses(region,addr):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        address = client_ec2.describe_addresses(
            PublicIps=addr
        )
        return address
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def release_address(region,alocid):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        address = client_ec2.release_address(
            AllocationId=alocid
        )
        return address
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def create_customer_gateway(region,name,asn,cert):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        customer_gateway = client_ec2.create_customer_gateway(
            BgpAsn=asn,
            CertificateArn=cert,
            Type='ipsec.1',
            TagSpecifications=[
                {
                    'ResourceType': 'customer-gateway',
                    'Tags': [
                        {
                            'Key': 'DeviceName',
                            'Value': name
                        }
                    ]
                }
            ]
        )
        return customer_gateway
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def describe_customer_gateways(region,name,asn,cert):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        customer_gateway = client_ec2.describe_customer_gateways(
            Filters=[
                {
                    'Name': 'tag:DeviceName',
                    'Values': [
                        name
                    ],
                    'Name': 'bgp-asn',
                    'Values': [
                        asn
                    ]
                        }
                    ]
                }
            ]
        )
        return customer_gateway
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def delete_customer_gateway(region,cgwid):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        customer_gateway = client_ec2.delete_customer_gateway(
            CustomerGatewayId=cgwid
        )
        return customer_gateway
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response
