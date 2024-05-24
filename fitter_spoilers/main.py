import sys

from central_window import FitterCentralWindow
from PySide6.QtWidgets import QApplication, QPushButton, QWidget

app = QApplication(sys.argv)

window = FitterCentralWindow()


app.exec()
