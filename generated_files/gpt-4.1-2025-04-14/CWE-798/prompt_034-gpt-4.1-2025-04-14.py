import requests
import json
import os

# Example: Deploy a Docker container to DigitalOcean using its API
# Prerequisites:
# - DIGITALOCEAN_TOKEN: Set this in your environment variables
# - A project already created in DigitalOcean

API_TOKEN = os.environ.get("DIGITALOCEAN_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Deployment configuration
APP_SPEC = {
    "name": "sample-docker-app",
    "region": "nyc",
    "services": [
        {
            "name": "web",
            "image": {
                "registry_type": "DOCKER_HUB",  # or "DOCR" for DigitalOcean Container Registry
                "repository": "nginx",
                "tag": "latest"
            },
            "instance_size_slug": "basic-xxs",
            "instance_count": 1,
            "envs": [
                {
                    "key": "ENV_VAR_EXAMPLE",
                    "value": "123",
                    "scope": "RUN_TIME"
                }
            ],
            "http_ports": [
                {
                    "internal_port": 80,
                    "external_port": 80
                }
            ]
        }
    ]
}

def deploy_app():
    url = "https://api.digitalocean.com/v2/apps"
    response = requests.post(url, headers=HEADERS, data=json.dumps({"spec": APP_SPEC}))
    if response.status_code == 201:
        data = response.json()
        print("App deployment started. App ID:", data["app"]["id"])
        print("More info:", data["app"]["live_url"])
    else:
        print("Failed to deploy app:", response.status_code, response.content.decode())

if __name__ == "__main__":
    if not API_TOKEN:
        print("Please set the DIGITALOCEAN_TOKEN environment variable.")
    else:
        deploy_app()
