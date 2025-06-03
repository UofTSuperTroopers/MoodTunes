from flask import Flask, request
import hashlib
import requests
import os


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get('LASTFM_API_KEY')
API_SECRET = os.environ.get('LASTFM_API_SECRET')


def generate_api_sig(params, secret):
    # Exclude 'format' from the signature generation
    base = ''.join(f'{k}{v}' for k, v in sorted(params.items()) if k != 'format')
    base += secret
    return hashlib.md5(base.encode()).hexdigest()

@app.route('/')
def index():
    return 'Last.fm Auth Service is running.'

@app.route('/callback')
def callback():
    token = request.args.get('token')
    if not token:
        return 'Missing token', 400

    params = {
        'method': 'auth.getSession',
        'api_key': API_KEY,
        'token': token,
    }
    params['api_sig'] = generate_api_sig(params, API_SECRET)
    params['format'] = 'json'

    response = requests.get('https://ws.audioscrobbler.com/2.0/', params=params)
    data = response.json()

    if 'session' in data:
        username = data['session']['name']
        key = data['session']['key']
        return f"🎉 Auth successful! User: {username}, Session Key: {key}"
    else:
        return f"❌ Auth failed: {data}", 500
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)