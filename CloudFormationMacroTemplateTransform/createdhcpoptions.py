import config
def main(name,PrivHZ):
    try:
        client_r53 = config.boto3.client('route53')
        zone = client_r53.get_hosted_zone(
            Id = PrivHZ
            )
        zonename = zone['HostedZone']['Name']
        config.fragment['Resources']['DhcpOptions'] = {}
        config.fragment['Resources']['DhcpOptions']['Type'] = 'AWS::EC2::DHCPOptions'
        config.fragment['Resources']['DhcpOptions']['Properties'] = {}
        config.fragment['Resources']['DhcpOptions']['Properties']['DomainName'] = zonename
        config.fragment['Resources']['DhcpOptions']['Properties']['DomainNameServers'] = [ 'AmazonProvidedDNS' ]
        config.fragment['Resources']['DhcpOptions']['Properties']['NtpServers'] = [ '169.254.169.123' ]
        config.fragment['Resources']['DhcpOptions']['Properties']['Tags'] = [{'Key': 'Name', 'Value': { "Fn::Join" : [ "-", [ "dhcopt", { "Ref": "AWS::StackName" } ] ] } } ]
        config.fragment['Resources']['DhcpOptions']['DependsOn'] = {}
        config.fragment['Resources']['DhcpOptions']['DependsOn'] = 'Vpc' + name
        config.fragment['Outputs']['DhcpOptions'] = {}
        config.fragment['Outputs']['DhcpOptions']['Description'] = 'DHCP Options ID'
        config.fragment['Outputs']['DhcpOptions']['Value'] = {'Ref': 'DhcpOptions'}
        config.fragment['Outputs']['DhcpOptions']['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , "DhcpOptions" ] ] } }
        config.fragment['Resources']['DhcpOptAssoc'] = {}
        config.fragment['Resources']['DhcpOptAssoc']['Type'] = 'AWS::EC2::VPCDHCPOptionsAssociation'
        config.fragment['Resources']['DhcpOptAssoc']['Properties'] = {}
        config.fragment['Resources']['DhcpOptAssoc']['Properties']['DhcpOptionsId'] =  {'Ref': 'DhcpOptions'}
        config.fragment['Resources']['DhcpOptAssoc']['Properties']['VpcId'] =  {'Ref': 'Vpc' + name}
        config.fragment['Resources']['DhcpOptAssoc']['DependsOn'] = {}
        config.fragment['Resources']['DhcpOptAssoc']['DependsOn'] = 'DhcpOptions'
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('VPC IPv6 Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response


