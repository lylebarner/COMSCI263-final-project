import requests

def download_and_display(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Failed to download content from {url}")

# Example usage
url = input("Enter the URL to download content from: ")
download_and_display(url)