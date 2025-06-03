from PyQt6.QtCore import QUrl, pyqtSlot
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import requests
import urllib.parse

LASTFM_API_KEY = '3d109d215b08689f69d5ab0040bc80b2'
CALLBACK_URL_PREFIX = "https://moodtunesuoft-863d99acf6d0.herokuapp.com/callback"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last.fm Auth")

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        # Connect to URL changes in the webview to intercept callback
        self.webview.urlChanged.connect(self.on_url_changed)

        # Start with the Last.fm auth URL (replace with your real key)
        auth_url = f'https://www.last.fm/api/auth?api_key={LASTFM_API_KEY}&cb={urllib.parse.quote(CALLBACK_URL_PREFIX)}'
        self.webview.load(QUrl(auth_url))

    @pyqtSlot(QUrl)
    def on_url_changed(self, url: QUrl):
        url_str = url.toString()
        print(f"Navigated to: {url_str}")

        if url_str.startswith(CALLBACK_URL_PREFIX):
            # Extract token param from URL query string
            query = urllib.parse.urlparse(url_str).query
            params = urllib.parse.parse_qs(query)
            token_list = params.get('token')
            if token_list:
                token = token_list[0]
                print(f"Token found: {token}")

                # Call your backend Flask service to get the session key
                # Change this URL to your deployed Flask app endpoint
                backend_url = f"https://moodtunesuoft-863d99acf6d0.herokuapp.com/callback?token={token}"
                try:
                    r = requests.get(backend_url)
                    r.raise_for_status()
                    # Show a simple message box with the response
                    QMessageBox.information(self, "Last.fm Auth", r.text)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to verify token: {e}")

                # Optionally, you can close the window or navigate elsewhere now
                # self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1900, 1600)
    w.show()
    sys.exit(app.exec())