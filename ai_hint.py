from PyQt5 import QtWidgets, QtCore

# графика
import ui.ai_hint_ui as ai_hint_ui

class HintWindow(QtWidgets.QWidget, ai_hint_ui.Ui_Form):
    def __init__(self, parent = None):
        super().__init__()
        self.setupUi(self)