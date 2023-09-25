#!/usr/bin/env python3

# import SDK
import boto3

# init sdk-client
aws_profile = 'academy'
aws_region = 'us-east-1'

session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

# Create an EC2 client
ec2_client = session.client('ec2')

# --------------------------------- #

# Get Image Id
images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04*']},
                                             {'Name': 'architecture', 'Values': ['x86_64']},
                                             {'Name': 'owner-alias', 'Values': ['amazon']}])

images_name_ids = [[item['CreationDate'], item['ImageId']] for item in images["Images"]]
image_name_id = images_name_ids[-1][1]

# Get Subnet
subnets = ec2_client.describe_subnets()
subnet_id = None
for subnet in subnets['Subnets']:
    if subnet['AvailabilityZone'] == 'us-east-1a':
        subnet_id = subnet['SubnetId']
        break

# --------------------------------- #

instance_params = {
    'ImageId': image_name_id,
    'InstanceType': 't3.micro',
    'KeyName': 'jarvis',
    'MinCount': 1,
    'MaxCount': 1,
    'SubnetId': subnet_id
}

response = ec2_client.run_instances(**instance_params)

# Extract the instance ID from the response
instance_id = response['Instances'][0]['InstanceId']

print(f"Launched EC2 instance with ID: {instance_id}")
