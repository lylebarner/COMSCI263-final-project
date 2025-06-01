import requests
import json

# Set the API key and endpoint
api_key = 'your_api_key_here'
api_endpoint = 'https://api.cloudprovider.com/v1/deploy'

# Docker container configuration
container_config = {
    "image": "nginx:latest",
    "name": "webserver",
    "ports": [
        {"containerPort": 80, "hostPort": 80, "protocol": "TCP"}
    ],
    "environmentVariables": {
        "ENV": "production"
    }
}

# Headers for the HTTP request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the request to deploy the container
response = requests.post(api_endpoint, headers=headers, data=json.dumps(container_config))

# Print the response from the API
print('Status Code:', response.status_code)
print('Response Body:', response.json())