import requests
import json

class DockerCloudDeployer:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def create_container(self, container_name, image_name):
        payload = {
            'name': container_name,
            'image': image_name
        }
        response = requests.post(
            f'{self.api_url}/containers',
            headers=self.headers,
            data=json.dumps(payload)
        )
        return response.json()

    def start_container(self, container_id):
        response = requests.post(
            f'{self.api_url}/containers/{container_id}/start',
            headers=self.headers
        )
        return response.json()

    def deploy_container(self, container_name, image_name):
        create_response = self.create_container(container_name, image_name)
        if create_response.get('id'):
            print(f'Container {container_name} created successfully.')
            start_response = self.start_container(create_response['id'])
            if start_response.get('status') == 'started':
                print(f'Container {container_name} started successfully.')
            else:
                print(f'Failed to start container {container_name}.')
        else:
            print('Failed to create container:', create_response)

if __name__ == '__main__':
    api_key = 'YOUR_API_KEY'
    api_url = 'https://api.your-cloud-platform.com'
    deployer = DockerCloudDeployer(api_key, api_url)

    container_name = 'my_container'
    image_name = 'my_image:latest'
    
    deployer.deploy_container(container_name, image_name)