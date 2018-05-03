#!/usr/bin/env python

import boto3

ec2 = boto3.resource('ec2')

# create VPC
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')

vpc.create_tags(Tags=[{"Key": "Name", "Value": "new_vpc"}])
vpc.wait_until_available()
print(vpc.id)

# create then attach internet gateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

route_table = None

for route_table in vpc.route_tables.all():  # There should only be one route table
    route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=ig.id)
    print(route_table.id)


# create subnet
subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
print(subnet.id)

# associate the route table with the subnet
route_table.associate_with_subnet(SubnetId=subnet.id)

# Create sec group
sec_group = ec2.create_security_group(
    GroupName='sec_group_1', Description='sec group', VpcId=vpc.id)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
)
print(sec_group.id)

# Create instance
instances = ec2.create_instances(
    ImageId='ami-7089b46d', InstanceType='t2.micro', MaxCount=1, MinCount=1,
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}])
instances[0].wait_until_running()

print(instances[0].id)
