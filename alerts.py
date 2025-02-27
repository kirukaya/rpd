from PyQt5 import QtWidgets, QtCore

# графика
import ui.alert_ui as alert_ui

class AlertWindow(QtWidgets.QDialog, alert_ui.Ui_Dialog):
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setupUi(self)