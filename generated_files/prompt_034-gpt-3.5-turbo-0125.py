import requests

def deploy_docker_container(api_url, container_image):
    data = {
        'image': container_image
    }
    response = requests.post(api_url, json=data)
    
    if response.status_code == 201:
        print('Container deployed successfully!')
    else:
        print('Failed to deploy container.')

# Example usage
api_url = 'https://cloud-platform.com/api/deploy'
container_image = 'your-docker-image:latest'
deploy_docker_container(api_url, container_image)