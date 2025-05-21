import boto3

def lambda_handler(event, context):
    region = event.get('region', 'us-east-1')
    action = event.get('action', '').lower()

    ec2 = boto3.client('ec2', region_name=region)

    if action == 'start':
        filters = [{'Name': 'instance-state-name', 'Values': ['stopped']}]
    elif action == 'stop':
        filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid action. Use "start" or "stop".'
        }

    response = ec2.describe_instances(Filters=filters)

    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if not instance_ids:
        return {
            'statusCode': 200,
            'body': f'No instances to {action} in region {region}'
        }

    if action == 'start':
        ec2.start_instances(InstanceIds=instance_ids)
    else:
        ec2.stop_instances(InstanceIds=instance_ids)

    return {
        'statusCode': 200,
        'body': f'{action.capitalize()}ed instances: {instance_ids}'
    }

