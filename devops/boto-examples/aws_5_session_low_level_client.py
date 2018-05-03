#!/usr/bin/env python

import boto3
import json
import pprint

session = boto3.Session()

ec2c = session.client('ec2')

zones = ec2c.describe_availability_zones()
pprint.pprint(zones, indent=2)

instances = ec2c.describe_instances()
pprint.pprint(instances, indent=2)