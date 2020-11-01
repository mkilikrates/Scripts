import config
def allocate_address(region,domain):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        response = client_ec2.allocate_address(
            Domain=domain
        )
        response["statusCode"] = "200"
        response["Reason"] = ("IP allocation succeed!")
        return response
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
        response = client_ec2.describe_addresses(
            PublicIps=addr
        )
        response["statusCode"] = "200"
        response["Reason"] = ("IP allocation succeed!")
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
        response = client_ec2.release_address(
            AllocationId=alocid
        )
        response["statusCode"] = "200"
        response["Reason"] = ("IP deallocation succeed!")
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
        response = client_ec2.create_customer_gateway(
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
        response["statusCode"] = "200"
        response["Reason"] = ("CGW Creation succeed!")
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
        response = client_ec2.describe_customer_gateways(
            Filters=[
                {
                    'Name': 'tag:DeviceName',
                    'Values': [
                        name
                    ],
                },
                {
                    'Name': 'bgp-asn',
                    'Values': [
                        asn
                    ]
                }
            ]
        )
        response["statusCode"] = "200"
        response["Reason"] = ("CGW description succeed!")
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
        response = client_ec2.delete_customer_gateway(
            CustomerGatewayId=cgwid
        )
        response["statusCode"] = "200"
        response["Reason"] = ("CGW removed succeed!")
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def create_vpn_connection(region,keylist):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        config.logger.info('Args: {}'.format(keylist))
        response = client_ec2.create_vpn_connection(**keylist)
        response["statusCode"] = "200"
        response["Reason"] = ("VPN Creation succeed!")
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

def delete_vpn_connection(region,vpnid):
    try:
        client_ec2 = config.boto3.client('ec2', region_name=region)
        response = client_ec2.delete_vpn_connection(
            VpnConnectionId=vpnid
        )
        response["statusCode"] = "200"
        response["Reason"] = ("VPN removed succeed!")
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["Reason"] = str(e)
    return response

