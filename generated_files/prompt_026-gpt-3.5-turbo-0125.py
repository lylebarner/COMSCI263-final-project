import requests

def download_and_display(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        print(response.text[:1000])  # Display a preview of the first 1000 characters
    else:
        print(f"Failed to download content from {url}")

# Example usage
url = input("Enter URL to download content:")
download_and_display(url)