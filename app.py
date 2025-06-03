from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
LASTFM_API_SECRET = os.environ.get("LASTFM_API_SECRET")


@app.route("/callback")
def callback():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "No token provided"}), 400

    # Exchange the token for a session key from Last.fm
    # Build the API signature required by Last.fm (md5 of sorted params + secret)
    # Reference: https://www.last.fm/api/webauth

    import hashlib

    # Parameters to sign
    params = {
        "api_key": LASTFM_API_KEY,
        "method": "auth.getSession",
        "token": token,
    }

    # Create the signature string by sorting params alphabetically by key, concat key+value
    signature_string = "".join(f"{k}{params[k]}" for k in sorted(params))
    signature_string += LASTFM_API_SECRET

    # MD5 hash the signature string
    api_sig = hashlib.md5(signature_string.encode("utf-8")).hexdigest()

    # Build request params including api_sig
    params["api_sig"] = api_sig
    params["format"] = "json"

    # Call Last.fm API to get session key
    resp = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)

    if resp.status_code != 200:
        return jsonify({"error": "Failed to contact Last.fm"}), 500

    data = resp.json()

    if "session" not in data:
        # If error from Last.fm API
        return jsonify({"message": data.get("message", "Unknown error"), "error": data.get("error", 0)}), 401

    session_key = data["session"]["key"]
    username = data["session"]["name"]

    # You *could* store the session_key & username in DB here for later use

    return jsonify({
        "session_key": session_key,
        "username": username,
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)