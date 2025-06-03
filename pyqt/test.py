from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    
    label = QLabel()
    self.label_ = label
    
    pixmap = QPixmap("pyqt/Images/faces.png")
    self.label_.setPixmap(pixmap)
    self.label_.setScaledContents(True)
    self.label_.resize(pixmap.size())
    
    
    self.setCentralWidget(self.label_)
    

app = QApplication([])
window = MainWindow()


window.show()

app.exec()

