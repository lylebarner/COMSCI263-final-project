import requests
from bs4 import BeautifulSoup

# Replace these with the target website's URLs and your credentials
LOGIN_URL = 'https://www.example.com/login'
DATA_URL = 'https://www.example.com/user/data'
USERNAME = 'your_username'
PASSWORD = 'your_password'

# Start a session to persist cookies
session = requests.Session()

# Get the login page to retrieve any hidden form fields (like CSRF tokens)
login_page = session.get(LOGIN_URL)
soup = BeautifulSoup(login_page.text, 'html.parser')

# Example of extracting a CSRF token if needed
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

# Prepare the payload with your credentials and any required hidden fields
payload = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrf_token': csrf_token
}

# Send a POST request to log in
response = session.post(LOGIN_URL, data=payload)

# Check if login was successful
if response.url == DATA_URL or response.status_code == 200:
    # Access the user-specific data page
    data_page = session.get(DATA_URL)
    data_soup = BeautifulSoup(data_page.text, 'html.parser')
    
    # Parse and extract the desired data
    # This will depend on the structure of the data page
    user_data = data_soup.find('div', {'id': 'user-data'})
    print(user_data.text)
else:
    print("Login failed")