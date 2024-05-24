import numpy as np
from hist_ansatze import hist_ansatze
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from mpl_canvas import MplCanvas, MplWidget
from PySide6.QtCore import QRect
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FitterHistWindow(QWidget):
    def __init__(self):
        super(FitterHistWindow, self).__init__()

        # Matplotlib Canvas
        self.mpl = MplCanvas()
        self.gridlayout = QGridLayout()
        self.gridlayout.addWidget(self.mpl, 1, 0, -1, 1)
        self.navbar = NavigationToolbar2QT(self.mpl)
        self.gridlayout.addWidget(self.navbar, 0, 0)

        # Load file button (needs open_dialog below)
        self.open_file_button = QPushButton(self, text="Open file")
        self.open_file_button.clicked.connect(self.open_dialog)
        self.gridlayout.addWidget(self.open_file_button, 0, 1)

        self.data = np.empty((0, 3))

        self.bins_box = QLineEdit()
        self.bins_box.setText("50")
        self.bins_box.textChanged.connect(self.update_plot_data)
        self.gridlayout.addWidget(self.bins_box, 2, 1)

        # Select Ansatz
        self.ansatz_select = QComboBox(self)
        for i, ansatz in enumerate(hist_ansatze):
            self.ansatz_select.addItem(ansatz.name)
        self.gridlayout.addWidget(self.ansatz_select, 1, 1)
        self.param_boxes = QWidget()
        self.param_boxes_layout = QGridLayout()
        self.param_boxes.setLayout(self.param_boxes_layout)
        self.param_boxes_children = []
        self.param_boxes_texts = []
        self.chi2_box = QLabel()
        self.gridlayout.addWidget(self.chi2_box, 3, 1)
        self.gridlayout.addWidget(self.param_boxes, 4, 1)
        self.ansatz_select.currentIndexChanged.connect(self.select_ansatz)

        # Apply Layout
        self.setLayout(self.gridlayout)

    # Open File
    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "CSV Files (*.csv)",
        )
        self.data = np.loadtxt(fname[0])
        self.update_plot_data()

    def select_ansatz(self):
        for widget in self.param_boxes_children:
            widget.setParent(None)

        index = self.ansatz_select.currentIndex()
        self.selected_ansatz = hist_ansatze[index]

        self.param_boxes_texts = []
        self.param_boxes_children = []

        func_label = QLabel()
        func_label.setText(self.selected_ansatz.form)
        self.param_boxes_layout.addWidget(func_label, 0, 0)

        self.param_boxes_children.append(func_label)

        for i in range(self.selected_ansatz.num_params):

            widget = ParamWidgets(self, i)

            self.param_boxes_texts.append(widget.text_box_val)
            self.param_boxes_children.append(widget)

            widget.text_box_val.textChanged.connect(self.plot_fit)

            self.param_boxes_layout.addWidget(widget, i + 1, 0)

    def update_plot_data(self):
        self.mpl.ax.clear()
        Nbins = int(self.bins_box.text())
        self.mpl.ax.hist(self.data, bins=Nbins, density=True)
        self.mpl.draw()

    def plot_fit(self):
        self.update_plot_data()
        x = np.linspace(self.data.min(), self.data.max(), 100)
        params = []
        for param in self.param_boxes_texts:
            try:
                params.append(float(param.text()))
            except ValueError:
                params.append(0.0)
        y = self.selected_ansatz.func(x, *params)
        chi2_fit = self.chi2(params)
        self.chi2_box.setText(f"chi2 / dof = {chi2_fit:.2f}")
        self.mpl.ax.plot(x, y)
        self.mpl.draw()

    def chi2(self, params):
        binned_data = np.histogram(
            self.data, bins=int(self.bins_box.text()), density=True
        )
        preds = self.selected_ansatz.func(
            binned_data[1][1:] - binned_data[1][:-1], *params
        )
        res = binned_data[0] - preds
        result = (res**2 / preds).sum()
        dof = len(binned_data[0]) - len(params)
        return result / dof


class ParamWidgets(QWidget):
    def __init__(self, parent=None, i=0):
        super(ParamWidgets, self).__init__(parent)
        self.gridlayout = QGridLayout()
        self.gridlayout.setColumnMinimumWidth(1, 100)
        self.label = QLabel(self)
        self.label.setText(chr(i + 97))
        self.labelmin = QLabel(self)
        self.labelmin.setText("Min")
        self.labelmax = QLabel(self)
        self.labelmax.setText("Max")
        self.text_box_val = QLineEdit(self)
        self.text_box_val.setText("0")

        self.text_box_min = QLineEdit(self)
        self.text_box_min.setText("0")

        self.text_box_max = QLineEdit(self)
        self.text_box_max.setText("10")

        self.slider = QSlider(Qt.Orientation.Horizontal, self)

        self.slider.setMinimum(0)
        self.slider.setMaximum(11)
        self.slider.setValue(0)

        self.slider.sliderMoved.connect(
            lambda: self.text_box_val.setText(
                str(
                    float(self.text_box_min.text())
                    + self.slider.value()
                    * (
                        float(self.text_box_max.text())
                        - float(self.text_box_min.text())
                    )
                    / 10
                )
            )
        )

        self.gridlayout.addWidget(self.label, 0, 0)
        self.gridlayout.addWidget(self.text_box_val, 0, 1)
        self.gridlayout.addWidget(self.labelmin, 1, 0)
        self.gridlayout.addWidget(self.labelmax, 1, 2)
        self.gridlayout.addWidget(self.text_box_min, 2, 0)
        self.gridlayout.addWidget(self.text_box_max, 2, 2)
        self.gridlayout.addWidget(self.slider, 2, 1)
        self.setLayout(self.gridlayout)
