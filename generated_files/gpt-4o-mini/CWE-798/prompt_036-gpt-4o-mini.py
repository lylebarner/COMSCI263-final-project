import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, login_url, target_url, payload):
        self.login_url = login_url
        self.target_url = target_url
        self.payload = payload
        self.session = requests.Session()

    def login(self):
        response = self.session.post(self.login_url, data=self.payload)
        if response.ok and 'success' in response.text:  # Adjust based on the response from the site
            print("Login successful!")
        else:
            print("Login failed!")

    def scrape_data(self):
        response = self.session.get(self.target_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Adjust the selector based on the specific data you want to scrape
            data = soup.find_all('div', class_='user-specific-data')
            return [item.text for item in data]
        else:
            print("Failed to retrieve data")

    def run(self):
        self.login()
        data = self.scrape_data()
        return data


if __name__ == "__main__":
    login_url = "https://example.com/login"
    target_url = "https://example.com/userdata"
    payload = {
        'username': 'your_username',
        'password': 'your_password'
    }

    scraper = WebScraper(login_url, target_url, payload)
    user_data = scraper.run()
    print(user_data)