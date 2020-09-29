import config
import base64
def create(Name,Cool,Capac,HCGP,Ltemp,LB,MinS,MaxS,Subnet,dep):
    # Where:
    # Name = Name to be used on resource name (LT + Name)
    # Cool = Cooldown, time between scaling activities
    # Capac = desired capacity
    # HCGP = HealthCheckGracePeriod
    # Ltemp = LaunchTemplate
    # LB = LoadBalancerNames
    # MinS = minimum size of the Auto Scaling group
    # MaxS = maximum size of the Auto Scaling group
    # Subnet = subnet list to deploy Auto Scaling group
    try:
        config.fragment['Resources']['ASG' + Name] = {}
        config.fragment['Resources']['ASG' + Name]['Type'] = 'AWS::AutoScaling::AutoScalingGroup'
        config.fragment['Resources']['ASG' + Name]['Properties'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['AutoScalingGroupName'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['AutoScalingGroupName'] = 'ASG' + Name
        if Cool != '':
            config.fragment['Resources']['ASG' + Name]['Properties']['Cooldown'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['Cooldown'] = Cool
        config.fragment['Resources']['ASG' + Name]['Properties']['DesiredCapacity'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['DesiredCapacity'] = Capac
        if HCGP != '':
            config.fragment['Resources']['ASG' + Name]['Properties']['HealthCheckGracePeriod'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['HealthCheckGracePeriod'] = HCGP
        config.fragment['Resources']['ASG' + Name]['Properties']['LaunchTemplate'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['LaunchTemplate']['LaunchTemplateId'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['LaunchTemplate']['LaunchTemplateId'] = {'Ref': Ltemp}
        config.fragment['Resources']['ASG' + Name]['Properties']['LaunchTemplate']['Version'] = {}
        config.fragment['Resources']['ASG' + Name]['Properties']['LaunchTemplate']['Version'] = { 'Fn::GetAtt' : [ Ltemp, 'LatestVersionNumber' ] }
        if MinS != '':
            config.fragment['Resources']['ASG' + Name]['Properties']['MinSize'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['MinSize'] = MinS
        else:
            config.fragment['Resources']['ASG' + Name]['Properties']['MinSize'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['MinSize'] = Capac
        if MaxS != '':
            config.fragment['Resources']['ASG' + Name]['Properties']['MaxSize'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['MaxSize'] = MaxS
        else:
            config.fragment['Resources']['ASG' + Name]['Properties']['MaxSize'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['MaxSize'] = Capac
        if LB != '':
            config.fragment['Resources']['ASG' + Name]['Properties']['TargetGroupARNs'] = []
            config.fragment['Resources']['ASG' + Name]['Properties']['TargetGroupARNs'] = LB
            config.fragment['Resources']['ASG' + Name]['Properties']['HealthCheckType'] = {}
            config.fragment['Resources']['ASG' + Name]['Properties']['HealthCheckType'] = 'ELB'
        if dep != '':
            config.fragment['Resources']['ASG' + Name]['DependsOn'] = {}
            config.fragment['Resources']['ASG' + Name]['DependsOn'] = dep
        config.fragment['Resources']['ASG' + Name]['Properties']['VPCZoneIdentifier'] = []
        config.fragment['Resources']['ASG' + Name]['Properties']['VPCZoneIdentifier'] = Subnet
        config.fragment['Resources']['ASG' + Name]['Properties']['Tags'] = [ { 'Key': 'Name', 'Value': { 'Ref': 'AWS::StackName' }, 'PropagateAtLaunch':'true' } ]
        config.fragment['Outputs']['ASG' + Name] = {}
        config.fragment['Outputs']['ASG' + Name]['Description'] = 'Auto Scale Group' + Name
        config.fragment['Outputs']['ASG' + Name]['Value'] = {'Ref': 'ASG' + Name}
        config.fragment['Outputs']['ASG' + Name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'ASG' + Name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Auto Scale Group ASG' + Name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response

def schdact(Name,asgname,capac,stime,etime,recr,dep):
    # Where:
    # Name = Name to be used on resource name
    # asgname = The name or Amazon Resource Name (ARN) of the Auto Scaling group
    # capac = capacity change (MaxSize, MinSize, or DesiredCapacity) and value like (DesiredCapacity:0,MinSize:0,MaxSize3)
    # stime = start time when action should be made
    # etime = end time when action should be made
    # recr = The recurring schedule for this action, in Unix cron syntax format
    # MinS = minimum size of the Auto Scaling group
    # MaxS = maximum size of the Auto Scaling group
    try:
        config.fragment['Resources']['ASGSCH' + Name] = {}
        config.fragment['Resources']['ASGSCH' + Name]['Type'] = 'AWS::AutoScaling::ScheduledAction'
        config.fragment['Resources']['ASGSCH' + Name]['Properties'] = {}
        config.fragment['Resources']['ASGSCH' + Name]['Properties']['AutoScalingGroupName'] = {}
        config.fragment['Resources']['ASGSCH' + Name]['Properties']['AutoScalingGroupName'] = asgname
        mcap = []
        if ',' in capac:
            mcap = list(capac.split(','))
        else:
            mcap.append(capac)
        for chg in mcap:
            chgc,chgn = chg.split(':',1)
            config.fragment['Resources']['ASGSCH' + Name]['Properties'][chgc] = {}
            config.fragment['Resources']['ASGSCH' + Name]['Properties'][chgc] = chgn
        if stime != '':
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['StartTime'] = {}
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['StartTime'] = stime
        if etime != '':
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['EndTime'] = {}
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['EndTime'] = etime
        if recr != '':
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['Recurrence'] = {}
            config.fragment['Resources']['ASGSCH' + Name]['Properties']['Recurrence'] = recr
        if dep != '':
            config.fragment['Resources']['ASGSCH' + Name]['DependsOn'] = {}
            config.fragment['Resources']['ASGSCH' + Name]['DependsOn'] = dep
        config.fragment['Outputs']['ASGSCH' + Name] = {}
        config.fragment['Outputs']['ASGSCH' + Name]['Description'] = 'Auto Scale Schedule Action' + Name
        config.fragment['Outputs']['ASGSCH' + Name]['Value'] = {'Ref': 'ASGSCH' + Name}
        config.fragment['Outputs']['ASGSCH' + Name]['Export'] = { "Name" : {"Fn::Join" : [ "-", [ { "Ref": "AWS::StackName" } , 'ASGSCH' + Name ] ] } }
        response = {}
        response["statusCode"] = "200"
        response["body"] = config.json.dumps('Auto Scale Group ASG' + Name + ' Creation Success!')
        return response
    except Exception as e:
        response = {}
        config.logger.error('ERROR: {}'.format(e))
        config.traceback.print_exc()
        response["statusCode"] = "500"
        response["body"] = str(e)
    return response