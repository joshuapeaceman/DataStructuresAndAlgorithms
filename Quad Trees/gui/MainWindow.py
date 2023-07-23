import os

import pyqtgraph
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'MainWindow.ui'), self)
        self.graphWidget = pyqtgraph.PlotWidget()
        self.graphWidget.setAspectLocked(1)
        self.mainFrame.addWidget(self.graphWidget)

    def getPlot(self):
        return self.graphWidget
