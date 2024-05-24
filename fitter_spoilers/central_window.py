from hist import FitterHistWindow
from PySide6.QtWidgets import QTabWidget
from scatter import FitterScatterWindow


class FitterCentralWindow(QTabWidget):
    def __init__(self):
        super(FitterCentralWindow, self).__init__()
        self.scatter_window = FitterScatterWindow()
        self.hist_window = FitterHistWindow()
        self.addTab(self.scatter_window, "Scatter")
        self.addTab(self.hist_window, "Histogram")

        self.show()
