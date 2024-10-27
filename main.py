from wsgiref.validate import check_status

import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-north-1")
ec2_resource = boto3.resource('ec2', region_name="eu-north-1")

# This will check on the instance  state
reservations = ec2_client.describe_instances()
print(reservations)
for reservation in reservations['Reservations']:
    instances = reservations['Instances']
    for instance in instances:
        print(f"Instance {instance['InstanceID']} is {instance['State']['Name']}")


# This method will check the instanceIDStatus and States and System Status
def check_instance_status():
    statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)
    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
    sys_status = status['SystemStatus']['Status']
    state = status['InstanceState']
    print(
        f"Instance {status['InstanceId']} is {status} with instance status {ins_status} and systemStatus is {sys_status}")

    schedule.every(5).minutes.do(check_instance_status)
    schedule.every().monday.at("7:00")

    while True:
        schedule.run_pending()
