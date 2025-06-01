import requests
from bs4 import BeautifulSoup

# --- Configuration ---
LOGIN_URL = 'https://example.com/login'
SCRAPE_URL = 'https://example.com/user/dashboard'
USERNAME = 'your_username'
PASSWORD = 'your_password'

# --- Start Session ---
session = requests.Session()

# --- Get Login Page (to fetch CSRF token if needed) ---
login_page = session.get(LOGIN_URL)
soup = BeautifulSoup(login_page.text, 'html.parser')

# Example: Extract CSRF token (modify selector as needed)
csrf_token = soup.find('input', {'name': 'csrf_token'})
token_value = csrf_token['value'] if csrf_token else ''

# --- Prepare Payload for Authentication ---
payload = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrf_token': token_value  # Remove if not needed
}

# --- Submit Login Form ---
response = session.post(LOGIN_URL, data=payload)
response.raise_for_status()

# --- Verify Login Success (modify as needed) ---
if "Login failed" in response.text or response.url == LOGIN_URL:
    print("Login failed.")
else:
    # --- Scrape Protected Page ---
    dashboard = session.get(SCRAPE_URL)
    dashboard.raise_for_status()
    soup = BeautifulSoup(dashboard.text, 'html.parser')

    # --- Parse & Print User-specific Data (adjust selector as needed) ---
    user_info = soup.select_one('.user-profile')
    print(user_info.get_text(strip=True) if user_info else "User info not found.")