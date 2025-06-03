from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from urllib.parse import urlparse, parse_qs

import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()


class AuthWindow(QWidget):
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
        api_key = os.environ.get('LASTFM_API_KEY')
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
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())