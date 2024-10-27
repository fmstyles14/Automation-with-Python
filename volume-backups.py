import boto3
import schedule
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

ec2_client = boto3.client('ec2', region_name="eu-north-1")

def create_volume_snapshots():
    ec2_client = boto3.client('ec2')

    try:
        volumes = ec2_client.describe_volumes(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['prod']
                }
            ]
        )
    except NoCredentialsError:
        print("Error: No AWS credentials found.")
        return
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
        return
    except ClientError as e:
        print(f"ClientError: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    for volume in volumes['Volumes']:
        try:
            new_snapshot = ec2_client.create_snapshot(
                VolumeId=volume['VolumeId']
            )
            print(new_snapshot)
        except ClientError as e:
            print(f"Failed to create snapshot for volume {volume['VolumeId']}: {e}")
        except Exception as e:
            print(f"Unexpected error while creating snapshot for volume {volume['VolumeId']}: {e}")

schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()
