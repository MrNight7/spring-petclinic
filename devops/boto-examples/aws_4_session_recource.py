#!/usr/bin/env python

import boto3

session = boto3.Session() # boto3.Session(profile_name=ireland)
ec2 = session.resource('ec2')
for instance in ec2.instances.all():
    print(instance)
    print(instance.hypervisor)

filter = {'Name': 'name', 'Values' : ['Amazon Linux AMI*']}
for image in ec2.images.filter(Filters = [filter]): print(image)