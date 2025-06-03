import requests
import hashlib
import os

from dotenv import load_dotenv

load_dotenv()


def generate_signature(params, api_secret = os.environ('API_SECRET')):
  sig = [f'{key}{val}' for key, val in sorted(params.items())]
  s = (''.join(sig) + api_secret).encode()
  return hashlib.md5(s).hexdigest()

p = {
  'method': 'auth.getSession',
  'api_key': os.environ('API_KEY'),
  'token': 'foo'
}