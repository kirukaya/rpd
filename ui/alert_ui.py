# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/alert.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(220, 72)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(220, 72))
        Dialog.setMaximumSize(QtCore.QSize(220, 72))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../icons/alert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonOk = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonOk.setGeometry(QtCore.QRect(75, 40, 70, 32))
        self.buttonOk.setOrientation(QtCore.Qt.Horizontal)
        self.buttonOk.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonOk.setObjectName("buttonOk")
        self.labelError = QtWidgets.QLabel(Dialog)
        self.labelError.setGeometry(QtCore.QRect(10, 10, 200, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelError.sizePolicy().hasHeightForWidth())
        self.labelError.setSizePolicy(sizePolicy)
        self.labelError.setMinimumSize(QtCore.QSize(200, 0))
        self.labelError.setMaximumSize(QtCore.QSize(200, 60))
        self.labelError.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelError.setWordWrap(True)
        self.labelError.setObjectName("labelError")

        self.retranslateUi(Dialog)
        self.buttonOk.accepted.connect(Dialog.accept) # type: ignore
        self.buttonOk.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ошибка"))
        self.labelError.setText(_translate("Dialog", "Заглушка для ошибки на две строки Заглушка для ошибки на две строки"))
