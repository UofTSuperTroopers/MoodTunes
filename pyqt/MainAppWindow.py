from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel




class MainAppWindow(QWidget):
  def __init__(self, session_key, username):
    super().__init__()
    
    self.setWindowTitle("MoodTunes App")
    
    
    layout = QVBoxLayout()
    
    welcome = QLabel(f"🎶 Welcome, {username}!\nSession: {session_key}")
    welcome.setWordWrap(True)
    
    layout.addWidget(welcome)
    self.setLayout(layout)