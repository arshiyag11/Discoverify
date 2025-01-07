import requests
import base64
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLIENT_ID = '00e6e8d966ab46ad99b29b92ea700493'
CLIENT_SECRET = '61242f5865e94e248ffaf98de29c7530'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# Define the URL for Spotify authentication with updated scopes
scopes = "user-modify-playback-state,playlist-read-private,user-read-playback-state"
auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scopes}"

# Start the selenium browser
browser = webdriver.Chrome()
browser.get(auth_url)

# Wait for a maximum of 120 seconds until the URL contains "code="
WebDriverWait(browser, 120).until(EC.url_contains("code="))

# Get the code from the current URL
url_after_login = browser.current_url
browser.close()

if "code=" in url_after_login:
    code = url_after_login.split('code=')[1]
else:
    print("Code not found in the redirected URL.")
    exit()

# Get the access token using the code
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('utf-8')).decode('utf-8')
payload = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}
headers = {"Authorization": f"Basic {auth_header}"}
response = requests.post(AUTH_URL, data=payload, headers=headers)
token = response.json().get('access_token')

# Save the token to a file
with open("spotify_token.txt", "w") as f:
    f.write(token)

print("Token saved to spotify_token.txt")
