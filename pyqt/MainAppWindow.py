from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDial, QSpinBox
from PyQt6.QtGui import QPixmap


class MainAppWindow(QWidget):
  def __init__(self, session_key, username):
    super().__init__()
    
    self.setWindowTitle("MoodTunes App")
    
    layout = QVBoxLayout()
    welcome = QLabel(f"🎶 Welcome, {username}!\nSession: {session_key}")
    
    face = QLabel()
    face.setPixmap(QPixmap("Images/faces.png"))
    face.setScaledContents(True)
    
    welcome.setWordWrap(True)

    layout.addWidget(welcome)
    layout.addWidget(face)
    
    self.setLayout(layout)