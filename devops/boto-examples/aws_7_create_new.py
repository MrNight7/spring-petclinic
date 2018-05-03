#!/usr/bin/env python

import boto3

low_level_client = boto3.client('ec2')

keypairs = low_level_client.describe_key_pairs()

# SSH Key
keyname = keypairs['KeyPairs'][0]['KeyName']

sec_groups = low_level_client.describe_security_groups(GroupNames=['launch-wizard-3'], DryRun=False)

# Security group id
sec_group_id = sec_groups['SecurityGroups'][0]['GroupId']

subnets = low_level_client.describe_subnets()
subnet_id = subnets['Subnets'][0]['SubnetId']

# Go to high level
ec2 = boto3.resource('ec2')

# AMI ID
ami_id = None
for image in ec2.images.filter(Filters = [{'Name': 'name', 'Values' : ['Amazon Linux AMI*']}]):
    ami_id = image.id
    #kostil :)
    break

instances = ec2.create_instances(
    ImageId=ami_id, InstanceType='t2.micro', MaxCount=1, MinCount=1, KeyName=keyname,
    NetworkInterfaces=[
        {'SubnetId': subnet_id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group_id]}
    ]
)
instances[0].create_tags(Tags=[{"Key": "Name", "Value": "Test"}])
instances[0].wait_until_running()

print(instances[0].id)

