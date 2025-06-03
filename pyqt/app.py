from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSlot
from urllib.parse import urlparse, parse_qs

import os
import requests
import sys
import hashlib

from MainAppWindow import MainAppWindow


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



class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last.fm Login")

        self.api_key = os.environ.get('LASTFM_API_KEY')
        self.token = get_token()['token']  # Get token first

        self.webview = QWebEngineView()
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 14px; padding: 10px;")
        self.info_label.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

        # Load auth URL with api_key and token
        auth_url = f"https://www.last.fm/api/auth?api_key={self.api_key}&token={self.token}"
        self.webview.load(QUrl(auth_url))
        self.webview.loadFinished.connect(self.on_load_finished)

    @pyqtSlot(bool)
    def on_load_finished(self, ok):
        if not ok:
            self.info_label.setText("❌ Failed to load page.")
            self.info_label.show()
            return
        
        self.webview.page().toHtml(self.check_page_content)

    def check_page_content(self, html):
        if "You have granted permission to" in html:
            self.info_label.setText("✅ Authorization complete. Fetching session key...")
            self.info_label.show()
            self.get_session_key()
            
            
    def on_url_changed(self, url: QUrl):
        # Check if the user has returned to the homepage after granting access
        if "last.fm/home" in url.toString():  # This is what users see after accepting
            self.info_label.setText("Authorization complete. You may now continue.")
            self.info_label.show()
            self.get_session_key()

    def get_session_key(self):
        api_secret = os.environ.get('LASTFM_API_SECRET')

        # Create signature for auth.getSession
        sig_str = f"api_key{self.api_key}methodauth.getSessiontoken{self.token}{api_secret}"
        api_sig = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

        params = {
            'method': 'auth.getSession',
            'api_key': self.api_key,
            'token': self.token,
            'api_sig': api_sig,
            'format': 'json'
        }

        response = requests.get('https://ws.audioscrobbler.com/2.0/', params=params)
        data = response.json()
        print(data)
        if 'session' in data:
            session_key = data['session']['key']
            username = data['session']['name']
            self.info_label.setText(f"✅ Authenticated!\nSession Key: {session_key}")
            self.session_key = session_key
            self.username = username
            
            self.launch_main_app()
        else:
            self.info_label.setText(f"❌ Auth failed: {data}")
        
        self.info_label.show()

    def launch_main_app(self):
        self.main_window = MainAppWindow(self.session_key, self.username)
        self.main_window.show()
        
        self.close()

class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last.fm Login")

        self.webview = QWebEngineView()
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 14px; padding: 10px;")
        self.info_label.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

        # Your callback URL registered in Last.fm app settings
        self.callback_prefix = "https://moodtunesuoft-863d99acf6d0.herokuapp.com/callback"
        self.webview.urlChanged.connect(self.on_url_changed)

        # Auth URL with just the API key, no 'cb' param
        # api_key = os.environ.get('LASTFM_API_KEY')
        
        api_key = get_token()['token']
        
        auth_url = f"https://www.last.fm/api/auth?api_key={api_key}"
        self.webview.load(QUrl(auth_url))

    def on_url_changed(self, url: QUrl):
        url_str = url.toString()
        print(f"[EVENT]: on_url_changed: url = {url_str}")

        # Check for your registered callback URL (where Last.fm sends token)
        if url_str.startswith(self.callback_prefix):
            query = urlparse(url_str).query
            params = parse_qs(query)
            token = params.get('token', [None])[0]

            if token:
                print(f"Extracted token: {token}")
                try:
                    # Exchange token for session key on your Flask backend
                    resp = requests.get(f"{self.callback_prefix}?token={token}")
                    if resp.status_code == 200:
                        json_data = resp.json()
                        session_key = json_data.get("session_key")
                        username = json_data.get("username")

                        if session_key and username:
                            self.webview.hide()
                            self.info_label.setText(f"🎉 Signed in as {username}!\n\nSession Key:\n{session_key}")
                            self.info_label.show()
                            self.adjustSize()
                        else:
                            self.show_error("⚠️ Missing session key or username in response.")
                    else:
                        self.show_error(f"❌ Auth failed: {resp.text}")
                except Exception as e:
                    self.show_error(f"❌ Exception during auth: {str(e)}")

    def show_error(self, message):
        self.webview.hide()
        self.info_label.setText(message)
        self.info_label.show()
        self.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = AuthWindow()
    login.show()
    
    sys.exit(app.exec())