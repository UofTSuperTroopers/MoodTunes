import requests
import hashlib
import os

from dotenv import load_dotenv

load_dotenv()


def get_token():
  api_key = os.environ.get('LASTFM_API_KEY')
  api_secret = os.environ.get('LASTFM_API_SECRET')

  sig_str = f'api_key{api_key}methodauth.getToken{api_secret}'
  api_sig = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

  params = {
    'method': 'auth.getToken',
    'api_key': api_key,
    'api_sig': api_sig,
    'format': 'json'
  }

  response = requests.get('https://ws.audioscrobbler.com/2.0/', params=params)
  token_data = response.json()

                            # Example return
  return token_data         # {'token': 'ZLdBzkV6PowxLPzmB9RA9kkOvsnvP5v8'} 


print(get_token())


def generate_signature(params, api_secret = os.environ.get('API_SECRET')):
  sig = [f'{key}{val}' for key, val in sorted(params.items())]
  s = (''.join(sig) + api_secret).encode()
  return hashlib.md5(s).hexdigest()

