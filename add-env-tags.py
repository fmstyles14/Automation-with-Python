import boto3

ec2_client_stockholm = boto3.client('ec2', region_name="eu-north-1")
ec2_resource_stockholm  = boto3.resource('ec2', region_name="eu-north-1")

ec2_client_paris = boto3.client('ec2', region_name="eu-west-3")
ec2_resource_paris = boto3.resource('ec2', region_name="eu-west-3")

instance_ids_stockholm  = []
instance_ids_paris = []

reservations_stockholm  = ec2_client_stockholm .describe_instances()['Reservations']
for res in reservations_stockholm :
    instances = res['Instances']
    for ins in instances:
        instance_ids_stockholm .append(ins['InstanceId'])


response = ec2_resource_stockholm .create_tags(
    Resources=instance_ids_stockholm,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

reservations_paris = ec2_client_paris.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instance_ids_paris.append(ins['InstanceId'])


response = ec2_resource_paris.create_tags(
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)