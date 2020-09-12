import config
import cvpne
def main():
    try:
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        desc = config.templateParameterValues['CVpnEName']
        vpc = config.templateParameterValues['VPC']
        sub = config.templateParameterValues['Subnet']
        sg = (config.templateParameterValues['SecurityGroup'])
        cidr = config.templateParameterValues['CIDR']
        certarn = (config.templateParameterValues['SrvCertArn'])
        clicertarn = config.templateParameterValues['CliCertArn']
        directoryID = config.templateParameterValues['DirectoryID']
        samlArn = config.templateParameterValues['SamlArn']
        loggrp = config.templateParameterValues['LogGrp']
        logstm = config.templateParameterValues['LogStr']
        dns = config.templateParameterValues['DNS']
        transp = config.templateParameterValues['Proto']
        port = config.templateParameterValues['Port']
        split = config.templateParameterValues['Split']
        routecidr = config.templateParameterValues['RouteCidr']
        authcidr = config.templateParameterValues['AuthCidr']
        group = config.templateParameterValues['Group']
        if directoryID != '':
            action = cvpne.create(desc,'Directory',directoryID,clicertarn,cidr,loggrp,logstm,dns,sg,certarn,split,transp,vpc,port)
            config.logger.info('Response: {}'.format(action))
        if samlArn != '':
            action = cvpne.create(desc,'Federated',samlArn,clicertarn,cidr,loggrp,logstm,dns,sg,certarn,split,transp,vpc,port)
            config.logger.info('Response: {}'.format(action))
        if samlArn == '' and directoryID == '':
            action = cvpne.create(desc,'','',clicertarn,cidr,loggrp,logstm,dns,sg,certarn,split,transp,vpc,port)
            config.logger.info('Response: {}'.format(action))
        action = cvpne.netass('CVPNE',sub)
        config.logger.info('Response: {}'.format(action))
        action = cvpne.route('CVPNE',sub,routecidr)
        config.logger.info('Response: {}'.format(action))
        action = cvpne.authrule('CVPNE',authcidr,group,sub)
        config.logger.info('Response: {}'.format(action))
        action = {}
        action["statusCode"] = "200"
        action["body"] = config.json.dumps('Template Update Success!')
        config.logger.info('Response: {}'.format(action))
        return action
    except Exception as e:
        action = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        action["statusCode"] = "500"
        action["body"] = str(e)
        config.logger.info('Response: {}'.format(action))
    return action
