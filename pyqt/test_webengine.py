import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last.fm Login")
        self.resize(1200, 800)

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        # Your API key here
        api_key = '3d109d215b08689f69d5ab0040bc80b2'
        # Last.fm auth URL
        auth_url = f"https://www.last.fm/api/auth?api_key={api_key}"

        self.webview.load(QUrl(auth_url))

        # Connect to URL change signal
        self.webview.urlChanged.connect(self.on_url_changed)

    def on_url_changed(self, url: QUrl):
        url_str = url.toString()
        print("Navigated to:", url_str)

        # Your callback URL (must match the one registered with Last.fm)
        # For example: https://yourdomain.com/callback or http://localhost/callback
        callback_prefix = "https://moodtunesuoft-863d99acf6d0.herokuapp.com/callback"

        if url_str.startswith(callback_prefix):
            # Extract token from URL query parameters
            from urllib.parse import urlparse, parse_qs

            query = urlparse(url_str).query
            params = parse_qs(query)
            token = params.get('token', [None])[0]

            if token:
                print("Token received:", token)
                
                self.close()
            else:
                print("No token found in callback URL")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())