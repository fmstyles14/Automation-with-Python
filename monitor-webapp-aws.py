import os
import time
import smtplib
import paramiko
import requests
import schedule
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
INSTANCE_ID = 'i-0abcd1234efgh5678'  # Replace with your AWS EC2 instance ID
REGION_NAME = 'eu-north-1'  # Replace with your AWS region


def restart_server_and_container():
    # Restart AWS EC2 instance
    print('Rebooting the server...')
    ec2 = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
                       region_name=REGION_NAME)
    ec2.reboot_instances(InstanceIds=[INSTANCE_ID])

    # Wait for the instance to be running again
    while True:
        response = ec2.describe_instance_status(InstanceIds=[INSTANCE_ID])
        instance_status = response['InstanceStatuses'][0]['InstanceState']['Name']
        if instance_status == 'running':
            time.sleep(5)
            restart_container()
            break


def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='your-aws-instance-public-ip', username='ec2-user',
                key_filename='/Users/new/.ssh/id_rsa')  # Adjust as needed
    stdin, stdout, stderr = ssh.exec_command('docker start cfd8ffb54f64')
    print(stdout.readlines())
    ssh.close()


def monitor_application():
    try:
        response = requests.get('http://your-aws-instance-public-ip:8080/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            msg = f'Application returned {response.status_code}'
            send_notification(msg)
            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()
