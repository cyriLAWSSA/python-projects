import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

# 1. Get all EBS snapshots
def get_all_ebs_snapshots(ec2_client):
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    return snapshots

# 2. Get all active EC2 instance IDs
def get_active_instance_ids(ec2_client):
    instances = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    return instance_ids

# 3-4. Iterate through each snapshot and delete if it's not attached to any volume or the volume is not attached to a running instance
def delete_unused_ebs_snapshots(ec2_client):
    snapshots = get_all_ebs_snapshots(ec2_client)
    active_instance_ids = get_active_instance_ids(ec2_client)

    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']

        # 5. Check if the volume still exists
        try:
            volume = ec2_client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
            if volume['State'] == 'available':
                # 4. Delete the snapshot if it's not attached to any volume
                print(f"Deleting unused EBS snapshot: {snapshot_id}")
                ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            else:
                # 3. Check if the volume is attached to a running instance
                for attachment in volume['Attachments']:
                    if attachment['InstanceId'] in active_instance_ids:
                        break
                else:
                    print(f"Deleting unused EBS snapshot: {snapshot_id}")
                    ec2_client.delete_snapshot(SnapshotId=snapshot_id)
        except Exception as e:
            # 6. The volume associated with the snapshot is not found (it might have been deleted)
            print(f"Error deleting snapshot {snapshot_id}: {e}")
            pass

# Example usage
delete_unused_ebs_snapshots(ec2_client)