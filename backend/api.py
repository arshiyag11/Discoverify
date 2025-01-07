from flask import Flask, jsonify
from shuffle import shuffle_and_add_to_queue
from flask_cors import CORS
from flask import request
import json
import os
import requests
import base64
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/gentoken', methods=['GET'])
def gentoken():
    # os.system('python3 token.py')

    CLIENT_ID = '2f16ee221f7640999e071fd4898da655'
    CLIENT_SECRET = 'b5c4f2e1e2bf41e09b6567f55974881b'
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
    # playlistID = 'https://open.spotify.com/playlist/37i9dQZF1EQp9BVPsNVof1?si=sKLEJ_Y0SwexVBAwwkqbWA&pi=u-EbPhU1U5QkmI'
    # shuffle_and_add_to_queue(playlistID, token)
    return jsonify({'token': token})

@app.route('/callback', methods=['GET'])
def callback():
    return "Callback route"

@app.route('/api/shuffle', methods=['POST'])
def shufflepost():
    data_dict = request.json
    playlistID = data_dict['ID']
    token = data_dict['Token']
    shuffle_and_add_to_queue(playlistID, token)
    return jsonify({'ID': playlistID})

# def shufflepost():
#     print("SharYA")
#     data_dict = request.json
#     playlistID = data_dict['ID']
#     token = data_dict['Token']
#     shuffle_and_add_to_queue(playlistID, token)
#     return jsonify({'ID': playlistID})

if __name__ == '__main__':
    app.run(debug=True)