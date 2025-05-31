import boto3
from botocore.exceptions import ClientError

def deploy_docker_container(
    cluster_name,
    service_name,
    task_family,
    container_name,
    image_uri,
    cpu,
    memory,
    desired_count,
    subnets,
    security_groups,
    region='us-east-1'
):
    ecs_client = boto3.client('ecs', region_name=region)

    try:
        # Register Task Definition
        response = ecs_client.register_task_definition(
            family=task_family,
            networkMode='awsvpc',
            containerDefinitions=[
                {
                    'name': container_name,
                    'image': image_uri,
                    'essential': True,
                    'memory': memory,
                    'cpu': cpu,
                    'portMappings': [
                        {
                            'containerPort': 80,
                            'hostPort': 80,
                            'protocol': 'tcp'
                        },
                    ],
                },
            ],
            requiresCompatibilities=['FARGATE'],
            cpu=str(cpu),
            memory=str(memory)
        )
        task_definition_arn = response['taskDefinition']['taskDefinitionArn']
        print(f"Registered task definition: {task_definition_arn}")

        # Create or Update Service
        try:
            ecs_client.create_service(
                cluster=cluster_name,
                serviceName=service_name,
                taskDefinition=task_definition_arn,
                desiredCount=desired_count,
                launchType='FARGATE',
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': subnets,
                        'securityGroups': security_groups,
                        'assignPublicIp': 'ENABLED'
                    }
                }
            )
            print(f"Service {service_name} created successfully.")
        except ecs_client.exceptions.ServiceAlreadyExistsException:
            ecs_client.update_service(
                cluster=cluster_name,
                service=service_name,
                taskDefinition=task_definition_arn,
                desiredCount=desired_count
            )
            print(f"Service {service_name} updated successfully.")

    except ClientError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    deploy_docker_container(
        cluster_name='my-cluster',
        service_name='my-service',
        task_family='my-task-family',
        container_name='my-container',
        image_uri='123456789012.dkr.ecr.us-east-1.amazonaws.com/my-image:latest',
        cpu=256,
        memory=512,
        desired_count=2,
        subnets=['subnet-abc12345', 'subnet-def67890'],
        security_groups=['sg-0123456789abcdef0']
    )