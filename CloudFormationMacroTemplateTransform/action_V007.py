import config
import createvpc
import gateway
import createroutetable
import route
import createsubnet
import createiamrole
import createinstprof
import securitygroup
import instance
import base64
def main():
    try:
        config.fragment['Resources'] = {}
        config.fragment['Outputs'] = {}
        vpcname = config.templateParameterValues['VpcName']
        vpccidr = {'Ref': 'VpcCidr'}
        vpcasn = {'Ref': 'VpcASN'}
        onpremname = config.templateParameterValues['OnpremName']
        onpremcidr = {'Ref': 'OnpremCidr'}
        onpremasn = {'Ref': 'OnpremASN'}
        ami = {'Ref': 'LatestAmiId'}
        traffsize = {'Ref': 'traffsize'}
        vpnsize = {'Ref': 'OnpremVPNsize'}
        vpnflav = config.templateParameterValues['OnpremVPNflav']
        # create VPC
        action = createvpc.main(vpcname,vpccidr,'No','')
        config.logger.info('Response: {}'.format(action))
        # create VPC Route Table
        action = createroutetable.main(vpcname,'Default','No')
        config.logger.info('Response: {}'.format(action))
        # create VPC igw
        action = gateway.igw(vpcname,'No','Vpc' + vpcname)
        config.logger.info('Response: {}'.format(action))
        # create VPC default route
        action = route.addv4('PubDefaultIpv4','0.0.0.0/0','RTDefault' + vpcname,'GatewayId','IGW' + vpcname)
        config.logger.info('Response: {}'.format(action))
        # create VPC subnets
        subcidr = { "Fn::Select" : [ 0, { "Fn::Cidr" : [ vpccidr, 6, 6 ] } ] }
        az = { "Fn::Select": [ 0, { "Fn::GetAZs": { "Ref" : "AWS::Region" } } ] }
        action = createsubnet.static(vpcname,'Subnet1',subcidr,az,'No','Pub','','RTDefault' + vpcname,'Vpc' + vpcname)
        config.logger.info('Response: {}'.format(action))
        subcidr = { "Fn::Select" : [ 1, { "Fn::Cidr" : [ vpccidr, 6, 6 ] } ] }
        az = { "Fn::Select": [ 1, { "Fn::GetAZs": { "Ref" : "AWS::Region" } } ] }
        action = createsubnet.static(vpcname,'Subnet2',subcidr,az,'No','Pub','','RTDefault' + vpcname,'Vpc' + vpcname)
        config.logger.info('Response: {}'.format(action))
        #create OnPrem
        action = createvpc.main(onpremname,onpremcidr,'No','')
        config.logger.info('Response: {}'.format(action))
        # create OnPrem Route Table
        action = createroutetable.main(onpremname,'Default','No')
        config.logger.info('Response: {}'.format(action))
        # create OnPrem igw
        action = gateway.igw(onpremname,'No','Vpc' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # create OnPrem default route
        action = route.addv4('PubDefaultIpv4','0.0.0.0/0','RTDefault' + onpremname,'GatewayId','IGW' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # create OnPrem subnets
        subcidr = { "Fn::Select" : [ 0, { "Fn::Cidr" : [ onpremcidr, 6, 6 ] } ] }
        az = { "Fn::Select": [ 0, { "Fn::GetAZs": { "Ref" : "AWS::Region" } } ] }
        action = createsubnet.static(onpremname,'Subnet1',subcidr,az,'No','Pub','','RTDefault' + onpremname,'Vpc' + onpremname)
        config.logger.info('Response: {}'.format(action))
        subcidr = { "Fn::Select" : [ 1, { "Fn::Cidr" : [ onpremcidr, 6, 6 ] } ] }
        az = { "Fn::Select": [ 1, { "Fn::GetAZs": { "Ref" : "AWS::Region" } } ] }
        action = createsubnet.static(onpremname,'Subnet2',subcidr,az,'No','Pub','','RTDefault' + onpremname,'Vpc' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # allocate EIP OnPrem VPNSRV
        action = gateway.eip(onpremname,'VPNSRV','Vpc' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # create vgw
        action = gateway.vgw('VGW',vpcasn,'MyVGW','ipsec.1',1,'Vpc' + vpcname)
        config.logger.info('Response: {}'.format(action))
        mygw = {'Ref': 'VGW'}
        # attach vgw on VPC
        vpcid = {'Ref' : 'Vpc' + vpcname}
        action = gateway.vgwattch('VGWATTC' + vpcname,mygw,vpcid)
        config.logger.info('Response: {}'.format(action))
        # route propagation from vgw
        rtids = [{'Ref' : 'RTDefault' + vpcname}]
        dep = ['VGWATTC' + vpcname, 'RTDefault' + vpcname]
        action = route.prop('MyGWRoutes',rtids,mygw,dep)
        config.logger.info('Response: {}'.format(action))
        # create cgw
        peerip = {'Ref': 'EIP' + onpremname + 'VPNSRV'}
        action = gateway.cgw('CGW',onpremasn,peerip,'ipsec.1',1,'EIP' + onpremname + 'VPNSRV')
        config.logger.info('Response: {}'.format(action))
        cgw = {'Ref': 'CGW'}
        vpntype = 'VGW'
        # create default vpn
        dep = ['VGW', 'CGW']
        action = gateway.vpn('VPN',cgw,1,mygw,vpntype,dep)
        config.logger.info('Response: {}'.format(action))
        # create iam role for deploy vpn
        pol = {
            "PolicyName": "DescribeVPNConn",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": [
                        "ec2:DescribeVpnConnections"
                    ],
                    "Resource": "*"
                }
                ]
            }
        }
        action = createiamrole.pol('DescribeVPNConn','ec2.amazonaws.com',pol,'')
        config.logger.info('Response: {}'.format(action))
        # create instance profile for vpn server
        action = createinstprof.main('InstProfVPNSrv','DescribeVPNConn','yes')
        config.logger.info('Response: {}'.format(action))
        # create security group for test instances
        action = securitygroup.create(vpcid,'InstanceTest' + vpcname)
        config.logger.info('Response: {}'.format(action))
        vpcid = {'Ref' : 'Vpc' + onpremname}
        action = securitygroup.create(vpcid,'InstanceTest' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # create security group for vpn server
        action = securitygroup.create(vpcid,'VPNSrv' + onpremname)
        config.logger.info('Response: {}'.format(action))
        # create rules to access test instances from AWS Office
        with open('zonemap.cfg') as zonefile:
            zonemap = config.json.load(zonefile)
            srcprefix = zonemap['Mappings']['RegionMap'][config.region]['PREFIXLIST']
            action = securitygroup.addingress('SecG' + 'InstanceTest' + vpcname,srcprefix,'SourcePrefixListId','-1','','','')
            config.logger.info('Response: {}'.format(action))
            action = securitygroup.addingress('SecG' + 'InstanceTest' + onpremname,srcprefix,'SourcePrefixListId','-1','','','')
            config.logger.info('Response: {}'.format(action))
        # create rules to VPN SRV
        action = securitygroup.addingress('SecG' + 'VPNSrv' + onpremname,'0.0.0.0/0','CidrIp','icmp','-1','-1','icmp')
        config.logger.info('Response: {}'.format(action))
        action = securitygroup.addingress('SecG' + 'VPNSrv' + onpremname,'0.0.0.0/0','CidrIp','udp','500','500','ike')
        config.logger.info('Response: {}'.format(action))
        action = securitygroup.addingress('SecG' + 'VPNSrv' + onpremname,'0.0.0.0/0','CidrIp','udp','4500','4500','IPsec NAT traversal')
        config.logger.info('Response: {}'.format(action))
        action = securitygroup.addingress('SecG' + 'VPNSrv' + onpremname,'0.0.0.0/0','CidrIp','50','','','ESP')
        config.logger.info('Response: {}'.format(action))
        # create instance test VPC
        vpcintproper = {}
        vpcintproper['DisableApiTermination'] = {}
        vpcintproper['DisableApiTermination'] = 'false'
        vpcintproper['InstanceInitiatedShutdownBehavior'] = {}
        vpcintproper['InstanceInitiatedShutdownBehavior'] = 'terminate'
        vpcintproper['NetworkInterfaces'] = []
        vpcintproper['NetworkInterfaces'] = [ {
            'AssociatePublicIpAddress' : 'true',
            'DeviceIndex' : 0,
            'DeleteOnTermination' : 'true',
            'SubnetId' : {'Ref' : vpcname + 'Subnet1' },
            'GroupSet' : [{ 'Ref': 'SecG' + 'InstanceTest' + vpcname}]
            } ]
        vpcintproper['ImageId'] = {}
        vpcintproper['ImageId'] = ami
        vpcintproper['InstanceType'] = {}
        vpcintproper['InstanceType'] = traffsize
        vpcintproper['Monitoring'] = {}
        vpcintproper['Monitoring'] = 'false'
        userdata = { "Fn::Base64": { "Fn::Join": [ "", [
           "#!/bin/bash -xe\n",
           "amazon-linux-extras install -y epel\n",
           "yum install -y openssl-devel xz xz-devel libffi-devel findutils wireshark tcpdump whois nuttcp iperf3 hping3 nmap sipcalc mtr bind-utils telnet\n",
           "yum update -y\n",
           "echo 'Ch@ng£m3' | passwd --stdin ec2-user\n",
           "echo 'ClientAliveInterval 60' | tee --append /etc/ssh/sshd_config\n",
           "echo 'ClientAliveCountMax 2' | tee --append /etc/ssh/sshd_config\n",
           "sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config\n",
           "systemctl restart sshd.service\n",
           "reboot\n" ] ] } }
        vpcintproper['UserData'] = userdata
        vpcintproper['Tags'] = []
        vpcintproper['Tags'] = [ {'Key': 'Name', 'Value': 'InstTest' + vpcname } ]
        dep = [vpcname + 'Subnet1', 'SecG' + 'InstanceTest' + vpcname]
        action = instance.create('InstTest' + vpcname,vpcintproper,dep)
        config.logger.info('Response: {}'.format(action))
        # create instance test Onprem
        onpremintproper = {}
        onpremintproper['DisableApiTermination'] = {}
        onpremintproper['DisableApiTermination'] = 'false'
        onpremintproper['InstanceInitiatedShutdownBehavior'] = {}
        onpremintproper['InstanceInitiatedShutdownBehavior'] = 'terminate'
        onpremintproper['NetworkInterfaces'] = []
        onpremintproper['NetworkInterfaces'] = [ {
            'AssociatePublicIpAddress' : 'true',
            'DeviceIndex' : 0,
            'DeleteOnTermination' : 'true',
            'SubnetId' : {'Ref' : onpremname + 'Subnet1' },
            'GroupSet' : [{ 'Ref': 'SecG' + 'InstanceTest' + onpremname}]
            } ]
        onpremintproper['ImageId'] = {}
        onpremintproper['ImageId'] = ami
        onpremintproper['InstanceType'] = {}
        onpremintproper['InstanceType'] = traffsize
        onpremintproper['Monitoring'] = {}
        onpremintproper['Monitoring'] = 'false'
        userdata = { "Fn::Base64": { "Fn::Join": [ "", [
           "#!/bin/bash -xe\n",
           "amazon-linux-extras install -y epel\n",
           "yum install -y openssl-devel xz xz-devel libffi-devel findutils wireshark tcpdump whois nuttcp iperf3 hping3 nmap sipcalc mtr bind-utils telnet\n",
           "yum update -y\n",
           "echo 'Ch@ng£m3' | passwd --stdin ec2-user\n",
           "echo 'ClientAliveInterval 60' | tee --append /etc/ssh/sshd_config\n",
           "echo 'ClientAliveCountMax 2' | tee --append /etc/ssh/sshd_config\n",
           "sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config\n",
           "systemctl restart sshd.service\n",
           "reboot\n" ] ] } }
        onpremintproper['UserData'] = userdata
        onpremintproper['Tags'] = []
        onpremintproper['Tags'] = [ {'Key': 'Name', 'Value': 'InstTest' + onpremname } ]
        dep = [onpremname + 'Subnet1', 'SecG' + 'InstanceTest' + onpremname]
        action = instance.create('InstTest' + onpremname,onpremintproper,dep)
        config.logger.info('Response: {}'.format(action))
        # create instance vpn Onprem
        onpremintproper = {}
        onpremintproper['DisableApiTermination'] = {}
        onpremintproper['DisableApiTermination'] = 'false'
        onpremintproper['InstanceInitiatedShutdownBehavior'] = {}
        onpremintproper['InstanceInitiatedShutdownBehavior'] = 'terminate'
        onpremintproper['SourceDestCheck'] = {}
        onpremintproper['SourceDestCheck'] = 'false'
        onpremintproper['IamInstanceProfile'] = {}
        onpremintproper['IamInstanceProfile'] = {'Ref' : 'InstProfVPNSrv'}
        onpremintproper['NetworkInterfaces'] = []
        onpremintproper['NetworkInterfaces'] = [ {
            'AssociatePublicIpAddress' : 'false',
            'DeviceIndex' : 0,
            'DeleteOnTermination' : 'true',
            'SubnetId' : {'Ref' : onpremname + 'Subnet1' },
            'GroupSet' : [{ 'Ref': 'SecG' + 'InstanceTest' + onpremname}, { 'Ref': 'SecG' + 'VPNSrv' + onpremname}]
            } ]
        onpremintproper['ImageId'] = {}
        onpremintproper['ImageId'] = ami
        onpremintproper['InstanceType'] = {}
        onpremintproper['InstanceType'] = vpnsize
        onpremintproper['Monitoring'] = {}
        onpremintproper['Monitoring'] = 'false'
        userdata = { "Fn::Base64": { "Fn::Join": [ "", [
           "#!/bin/bash -xe\n",
           "amazon-linux-extras install -y epel\n",
           "yum install -y strongswan quagga python2-boto3 python-xmltodict git\n",
           "aws configure --profile default set region ", { "Ref" : "AWS::Region" }, "\n",
           "yum update -y\n",
           "git clone https://github.com/mkilikrates/launchvpn.git\n",
           "cd launchvpn\n",
           "./vpn-tunnel.py default ", { "Ref": "VPN" }, " dynamic\n",
           "sleep 3\n",
           "sed -i 's/\\ -r a.b.c.d\\/e//g' ipsec_conf.txt\n",
           "cat ipsec_conf.txt >> /etc/strongswan/ipsec.conf\n",
           "cat ipsec.secrets.txt >> /etc/strongswan/ipsec.secrets\n",
           "sed -i '/^router bgp/a \\ network ", { "Ref": "OnpremCidr" }, "' /launchvpn/bgpd.conf.txt\n",
           "export GATEWAY=$(/sbin/ip route | awk '/default/ { print $3 }')\n",
           "route add -net ", { "Ref": "OnpremCidr" }, " gw $GATEWAY\n",
           "echo ", { "Ref": "OnpremCidr" }, " via $GATEWAY >>/etc/sysconfig/network-scripts/route-eth0\n",
           "cat bgpd.conf.txt >> /etc/quagga/bgpd.conf\n",
           "cp -f aws-updown.sh /etc/strongswan/ipsec.d/\n",
           "cp -f heartbeat.sh /etc/strongswan/ipsec.d/\n",
           "cd ..\n",
           "rm -rf /launchvpn\n",
           "systemctl enable strongswan\n",
           "systemctl enable zebra\n",
           "systemctl enable bgpd\n",
           "echo 'Ch@ng£m3' | passwd --stdin ec2-user\n",
           "echo 'ClientAliveInterval 60' | tee --append /etc/ssh/sshd_config\n",
           "echo 'ClientAliveCountMax 2' | tee --append /etc/ssh/sshd_config\n",
           "sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config\n",
           "systemctl restart sshd.service\n",
           "reboot\n" ] ] } }
        onpremintproper['UserData'] = userdata
        onpremintproper['Tags'] = []
        onpremintproper['Tags'] = [ {'Key': 'Name', 'Value': 'VPNSRV' + onpremname } ]
        dep = [onpremname + 'Subnet1', 'SecG' + 'InstanceTest' + onpremname, 'InstProfVPNSrv']
        action = instance.create('VPNSRV' + onpremname,onpremintproper,dep)
        config.logger.info('Response: {}'.format(action))
        # attach EIP on VPNSRV
        allocid = {'Fn::GetAtt' : ['EIP' + onpremname + 'VPNSRV', 'AllocationId']}
        instid = {'Ref' : 'VPNSRV' + onpremname}
        dep = ['VPNSRV' + onpremname, 'EIP' + onpremname + 'VPNSRV']
        action = gateway.eipass('VPNSRV',instid,'','',allocid,dep)
        config.logger.info('Response: {}'.format(action))
        # create route to VPC on Onprem
        vpninstid = {'Ref' : 'VPNSRV' + onpremname}
        action = route.addv4(vpcname,vpccidr,'RTDefault' + onpremname,'InstanceId',vpninstid)
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
