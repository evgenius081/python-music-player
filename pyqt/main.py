from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication

app = QApplication()
window = QWindow()
window.setFixedWidth(1024)
window.setFixedHeight(768)
window.show()
app.exec()
