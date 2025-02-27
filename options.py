from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont

# графика
import ui.options_ui as options_ui

# модули
import modules.files_m as filesModule

class PreferencesWindow(QtWidgets.QWidget, options_ui.Ui_Form):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setupUi(self)

        self.fontSizeSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.fontSizeSlider.setRange(10, 12)
        self.fontSizeSlider.setTickInterval(1)
        self.fontSizeSlider.valueChanged.connect(self.updateFontSize)

        self.okButton.clicked.connect(self.savePreferences)  
    

    def updateFontSize(self, value):
        self.lineFontSize.setText(str(value))

    def savePreferences(self):
        config = filesModule.loadPreferences()
        config.set('main', 'font-size', self.lineFontSize.text())
        config.set('gpt', 'cat-id', self.lineID.text())
        config.set('gpt', 'api-key', self.lineAPI.text())
        with open('config.ini', 'w') as f:
            config.write(f)

        self.parent.setFontSize()

        self.close()