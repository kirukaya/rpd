import sys
from math import floor, ceil
import re

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QFont
import pyautogui

# графика
import ui.main_ui as main_ui

# окна
from options import PreferencesWindow
from alerts import AlertWindow
from ai_hint import HintWindow

# модули
from modules.import_m import importExcel, importCsv
from modules.yagpt_m import requestCompetenciesIndicators, requestCompetenciesResults, requestThemes, requestThemeDescription, requestSeminarQuestions, requestHomeworkQuestions, requestHintThemesHours
import modules.files_m as filesModule
from modules.export_m import exportFileRpd, exportFileBrs
import modules.bd_m as dataBaseModule


class RpdWindow(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # название окна
        self.windowTitle = "РПД Менеджер[*]"
        self.setWindowTitle(self.windowTitle)

        # прочие окна
        self.preferences = PreferencesWindow(self)
        self.alert = AlertWindow(self)
        self.hint = HintWindow(self)
        self.setFontSize()
        
        # менюбар
        self.connectMenubar()

        # основное: подключение кнопок (помимо менюбара), настройка таблиц, полей
        self.connectButtons()
        self.prepareTables()
        self.resizeTables(first = True)
        dataBaseModule.getFaculties(self)

        # сохранение и загрузка
        self.fileName = None
        self.manageFields("connect") # подключение отслеживания для виджетов,
                                     #изменение которых влияет на сохранение и загрузку
        # удобство пользования
        self.revertBackup = ""
        self.lastSelected = ""

    def connectMenubar(self):
        fileDialog = QtWidgets.QFileDialog()
        self.actionNew.triggered.connect(lambda: filesModule.newFile(self, fileDialog))
        self.actionOpen.triggered.connect(lambda: filesModule.openFile(self, fileDialog))
        self.actionSave.triggered.connect(lambda: filesModule.saveFile(self, fileDialog))
        self.actionSaveAs.triggered.connect(lambda: filesModule.saveAsFile(self, fileDialog))
        self.actionClose.triggered.connect(lambda: filesModule.closeFile(self))
        self.actionExit.triggered.connect(app.quit)
        self.actionPreferences.triggered.connect(self.openWindowPreferences)

        self.actionUndo.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'z'))
        self.actionRedo.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'y'))
        self.actionCut.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'x'))
        self.actionCopy.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'c'))
        self.actionPaste.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'v'))
        self.actionDelete.triggered.connect(lambda: pyautogui.hotkey('del'))
        self.actionSelectAll.triggered.connect(lambda: pyautogui.hotkey('ctrl', 'a'))


        self.actionTab0.triggered.connect(lambda: self.tabWidget.setTabVisible(0, self.actionTab0.isChecked()))
        self.actionTab1.triggered.connect(lambda: self.tabWidget.setTabVisible(1, self.actionTab1.isChecked()))
        self.actionTab2.triggered.connect(lambda: self.tabWidget.setTabVisible(2, self.actionTab2.isChecked()))
        self.actionTab3.triggered.connect(lambda: self.tabWidget.setTabVisible(3, self.actionTab3.isChecked()))
        self.actionTab4.triggered.connect(lambda: self.tabWidget.setTabVisible(4, self.actionTab4.isChecked()))
        self.actionTab5.triggered.connect(lambda: self.tabWidget.setTabVisible(5, self.actionTab5.isChecked()))

        self.menuToolbars.setEnabled(False)

    def connectButtons(self):
        fileDialog = QtWidgets.QFileDialog()
        self.importButton.clicked.connect(self.importSyllabus)  
        self.refreshPlaceButton.clicked.connect(self.composePlace)

        self.submitButtonComp.clicked.connect(self.submitCompetencies)
        self.generateButtonComp.clicked.connect(self.generateCompetencies)
        self.revertButtonComp.clicked.connect(self.revertCompetencies)

        self.submitButtonThemes.clicked.connect(self.submitThemes)
        self.generateButtonThemes.clicked.connect(self.generateThemes)
        self.revertButtonThemes.clicked.connect(self.revertThemes)

        self.submitButtonThemes2.clicked.connect(self.submitThemes2)
        self.generateButtonThemes2.clicked.connect(self.generateThemes2)
        self.revertButtonThemes2.clicked.connect(self.revertThemes2)

        self.generateButtonThemesHours.clicked.connect(self.generateThemesHours)
        self.refillButton.clicked.connect(self.fillEvenlyThemesHours)

        self.importTestsButton.clicked.connect(self.importTests)
        self.analyzeTestsButton.clicked.connect(self.analyzeTests)

        self.filePathButton.clicked.connect(lambda: filesModule.chooseExportPath(self, fileDialog, "rpd"))
        self.exportButton.clicked.connect(lambda: self.prepareExport("rpd"))
        self.filePathButton2.clicked.connect(lambda: filesModule.chooseExportPath(self, fileDialog, "brs"))
        self.exportButton2.clicked.connect(lambda: self.prepareExport("brs"))

    def prepareExport(self, document):
        self.actionSave.trigger()
        if not self.isWindowModified() and self.fileName:
            data = window.manageFields("save")
            format = 'docx'
            if self.comboBoxFormat.currentText() == ".pdf":
                format = 'pdf'
            if document == "rpd":
                exportFileRpd(self.lineFilePath.text(), data, self.radioButtonFull.isChecked(), format)
            elif document == "brs":
                exportFileBrs(self.lineFilePath2.text(), data)

    def prepareTables(self):
        self.tableHours.verticalHeader().hide()
        self.tableHours.setSpan(5, 0, 1, 2)
        self.tableHours.setSpan(6, 0, 1, 2)
        header = self.tableCompetencies.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(0, 100)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(1, 150)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(2, 220)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(3, 263) # 270
        header = self.tableDost.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(0, 150)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(1, 594)
        self.tableThemesHours.horizontalHeader().hide()
        self.tableThemesHoursFooter.horizontalHeader().hide()
        self.tableThemesHours.setItem(0, 0, self.customQTableWidgetItem("""Наименование
тем (разделов)
дисциплины""", editable=False))
        self.tableThemesHours.setSpan(0, 0, 3, 1)
        self.tableThemesHours.setItem(0, 1, self.customQTableWidgetItem("""Трудоемкость в часах""", editable=False))
        self.tableThemesHours.setSpan(0, 1, 1, 5)
        self.tableThemesHours.setItem(1, 1, self.customQTableWidgetItem("""Всего""", editable=False))
        self.tableThemesHours.setSpan(1, 1, 2, 1)
        self.tableThemesHours.setItem(1, 2, self.customQTableWidgetItem("""Контактная работа -
Аудиторная работа""", editable=False))
        self.tableThemesHours.setSpan(1, 2, 1, 3)
        self.tableThemesHours.setItem(2, 2, self.customQTableWidgetItem("""Общая,
в
т.ч.:""", editable=False))
        self.tableThemesHours.setItem(2, 3, self.customQTableWidgetItem("""Лекции""", editable=False))
        self.tableThemesHours.setItem(2, 4, self.customQTableWidgetItem("""Семинары,
практические занятия""", editable=False))
        self.tableThemesHours.setItem(1, 5, self.customQTableWidgetItem("""Самостоятельная
работа""", editable=False))
        self.tableThemesHours.setSpan(1, 5, 2, 1)
        self.tableThemesHours.setItem(0, 6, self.customQTableWidgetItem("""Формы текущего
контроля
успеваемости""", editable=False))
        self.tableThemesHours.setSpan(0, 6, 3, 1)
        self.tableThemesHoursFooter.setItem(0, 0, self.customQTableWidgetItem("""В целом по дисциплине""", editable=False))
        self.tableThemesHoursFooter.setItem(1, 0, self.customQTableWidgetItem("""Итого в %""", editable=False))
        for table in [self.tableThemesHours, self.tableThemesHoursFooter]:
            table.setColumnWidth(0, 200)
            table.setColumnWidth(1, 50)
            table.setColumnWidth(2, 60)
            table.setColumnWidth(3, 60)
            table.setColumnWidth(4, 90)
            table.setColumnWidth(5, 120)
            table.setColumnWidth(6, 150)
            header = table.verticalHeader()
            for i in range(table.rowCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
        self.tableThemesHours.setColumnWidth(0, 198)
        self.tableThemesHours.setRowHeight(1, 40)
        self.tableThemesHours.setRowHeight(2, 60)
        header = self.tableBrs1.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        self.tableBrs1.setColumnWidth(0, 100)
        self.tableBrs1.setColumnWidth(1, 418)
        self.tableBrs1.setColumnWidth(2, 100)
        self.tableBrs1.setColumnWidth(3, 100)


        self.tableCompetencies.doubleClicked.connect(self.doubleClickCompetencies)
        self.tableThemes.doubleClicked.connect(self.doubleClickThemes)

    def openAlert(self, text):
        self.alert.labelError.setText(text)
        QApplication.beep()
        self.alert.show()
        point = self.pos()
        self.alert.move(point.x()+290, point.y()+264)

    def openWindowPreferences(self):
        config = filesModule.loadPreferences()
        self.preferences.fontSizeSlider.setValue(int(config.get("main", "font-size")))
        self.preferences.lineFontSize.setText(config.get("main", "font-size"))
        self.preferences.lineID.setText(config.get("gpt", "cat-id"))
        self.preferences.lineAPI.setText(config.get("gpt", "api-key"))
        self.preferences.show()
        point = self.pos()
        self.preferences.move(point.x()+200, point.y()+210)

    def analyzeTests(self):
        data = []
        try:
            for row_i in range(self.tableTests.rowCount()):
                if self.tableTests.item(row_i, 0).text() != "":
                    element = []
                    # time = self.tableTests.item(row_i, 7).text()
                    # result = re.findall("\d+", time)
                    # if len(result) > 1:
                    #     element.append(int(result[0])*60+int(result[1]))
                    element.append(float(self.tableTests.item(row_i, 8).text().replace(',', '.')))
                    for i in range(9, 14):
                        if self.tableTests.item(row_i, i).text() != "":
                            element.append(float(self.tableTests.item(row_i, i).text().replace(',', '.')))
                    data.append(element)
        except:
            self.openAlert('Неправильный формат таблицы')
        if data != []:
            maxx = 0
            avg = 0
            count = 0
            for i in range(len(data)):
                if data[i][0] > maxx: maxx = data[i][0]
                avg += data[i][0]
                count += 1
            avg = avg / count
            if avg/maxx > 0.7:
                answer = "Тема не является пробельной. Значительная часть студентов усвоила материал."
            else:
                answer = "Тема является пробельной. Необходимо выделить больше часов на эту тему или переработать методы обучения."

            self.hint.textBrowserAI.setText(answer)
            self.hint.show()
    
    def importTests(self):
        fileDialog = QtWidgets.QFileDialog()
        result = importCsv(fileDialog, self)
        if result:
            for i in range(self.tableTests.rowCount()):
                for j in range(self.tableTests.columnCount()):
                    self.tableTests.item(i, j).setText("")
            for i in range(1, len(result)):
                for j in range(len(result[0])):
                    self.tableTests.item(i-1, j).setText(result[i][j])

    def importSyllabus(self):
        title = self.lineTitle.text()
        if title != "":
            fileDialog = QtWidgets.QFileDialog()
            result = importExcel(fileDialog, self, title)

            if result: # обработка и хранение данных
                self.lineTitle.setText(result[1].replace("*", ""))
                self.comboBoxDepartment.setCurrentText(result[2])
                comps = result[3].split(", ")
                competenciesDefinitions = dataBaseModule.getCompetencies()

                # почиситть таблицы
                for i in range(self.tableCompetencies.rowCount()):
                    self.tableCompetencies.item(i, 0).setText("")
                    if competenciesDefinitions:
                        self.tableCompetencies.item(i, 1).setText("")
                
                for i in range(self.tableDost.rowCount()):
                    self.tableDost.item(i, 0).setText("")

                # заполнять
                for i in range(len(comps)):
                    self.tableCompetencies.item(i, 0).setText(comps[i])
                    self.tableDost.item(i, 0).setText(comps[i])

                    for code, definition in competenciesDefinitions:
                        if comps[i] == code:
                            self.tableCompetencies.item(i, 1).setText(definition)

                data = [result[12:18], [result[18]]+result[19:23], [result[18]]+result[23:27], [result[27]]+result[28:32], [result[27]]+result[32:36],
                        [result[36]]+result[37:41], [result[36]]+result[41:45], [result[45]]+result[46:50], [result[45]]+result[50:54]]  
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        if not data[i][j]:
                            data[i][j] = 0
                
                for i in range(self.tableHours.rowCount()):
                    for j in range(1, self.tableHours.columnCount()):
                        self.tableHours.item(i, j).setText("")

                self.tableHours.setItem(0, 1, self.customQTableWidgetItem(f"{data[0][0]}/{data[0][1]}"))
                for j in range(1, 5):
                    self.tableHours.setItem(j, 1, self.customQTableWidgetItem(f"{data[0][j+1]}"))
                for i in range(1, 9):
                    if data[i][3]:
                        self.tableHours.setItem(0, i+1, self.customQTableWidgetItem(f"{data[i][2]+data[i][3]+data[i][4]}"))
                        self.tableHours.setItem(1, i+1, self.customQTableWidgetItem(f"{data[i][2]+data[i][3]}"))
                        self.tableHours.setItem(2, i+1, self.customQTableWidgetItem(f"{data[i][2]}"))
                        self.tableHours.setItem(3, i+1, self.customQTableWidgetItem(f"{data[i][3]}"))
                        self.tableHours.setItem(4, i+1, self.customQTableWidgetItem(f"{data[i][4]}"))
                
                dataExams = result[4:11]
                exams = []
                types = ["экзамен", "зачет", "курсовая работа", "расчетно-аналитическая работа", 
                        "домашнее творческое задание", "контрольная работа", "эссе"]
            
                for exam in zip(dataExams, types):
                    if exam[0] and exam[1] in ["экзамен", "зачет"]:
                        exams.append([types.index(exam[1]), 6, exam[1]])
                    elif exam[0]:
                        exams.append([types.index(exam[1]), 5, exam[1]])

                multiplecc = True
                for e in exams:
                    i = e[0]
                    row = e[1]
                    caption = e[2]
                    if e[1] == 5:
                        cc = caption
                    if "," in dataExams[i]:
                        splitted = dataExams[i].split(",") 
                        for value in splitted:
                            self.tableHours.setItem(row, int(value)+1, self.customQTableWidgetItem(caption))
                    elif "-" in dataExams[i]:
                        splitted = dataExams[i].split("-")
                        for i in range(int(splitted[0]), int(splitted[1])+1):
                            self.tableHours.setItem(row, i+1, self.customQTableWidgetItem(caption))
                    else:
                        if e[1] == 5:
                            multiplecc = False
                        self.tableHours.setItem(row, int(dataExams[i])+1, self.customQTableWidgetItem(caption))

                # часы на темы
                types2 = ["курсовая работа", "расчетно-аналитическая работа", "домашнее творческое задание", "контрольная работа", "эссе"]
                types3 = ["курсовая работа", "расчетно-аналитические работы", "домашние творческие задания", "контрольные работы", "эссе"]
                for i in range(1,6):
                    self.tableThemesHoursFooter.item(0, i).setText(str(data[0][i]))
                if multiplecc:
                    self.tableThemesHoursFooter.item(0, 6).setText("Согласно учебному плану: "+types3[types2.index(cc)])
                else:
                    self.tableThemesHoursFooter.item(0, 6).setText("Согласно учебному плану: "+cc)
                
                data = [data[0][2]/data[0][1], data[0][3]/data[0][2], data[0][4]/data[0][2], data[0][5]/data[0][1]]
                for i in range(2, 6):
                    self.tableThemesHoursFooter.item(1, i).setText(str(round(data[i-2]*100)))
        else:
            self.openAlert("Введите название дисциплины для импорта из учебного плана")

    def composePlace(self):
        if self.lineTitle.text() == "":
            self.openAlert('Сначала укажите наименование дисциплины')
        elif self.lineDoT.text() == "":
            self.openAlert('Сначала укажите направление подготовки')
        else:
            self.textEditPlace.setText(f"Дисциплина «{self.lineTitle.text()}» относится к Общепрофессиональному циклу дисциплин по направлению подготовки {self.lineDoT.text()}")

    def manageFields(self, action, data=None):
        # Общий метод для управления полями, позводляющий: 1) подключить отслеживаине изменений; 2) взять значения; 3) установить значения; полей.
        # Действия: "connect" подключает, "save" берет значения для дальнейшего сохранения, "load" наоборот устанавлиает значения. 
        # print(data)
        layouts = [self.horizontalLayout11, # лейауты, в которых находятся виджеты с данными
                   self.horizontalLayout12,
                   self.formLayout11,
                   self.formLayout21,
                   self.verticalLayout31,
                   self.formLayout31,
                   self.verticalLayout33,
                   self.verticalLayout34,
                   self.verticalLayout41,
                   self.verticalLayout42,
                   self.formLayout41,
                   self.formLayout42,
                   self.formLayout43,
                   self.formLayout51,
                   self.horizontalLayout51,
                   self.verticalLayout61,
                   self.horizontalLayout61]
        if action == "save":
            data = []
        if action == "load":
            increment = 0
        for layout in layouts:
            for i_widget in range(layout.count()): # считаем дочерние элементы и проходимся по ним
                child = layout.itemAt(i_widget)
                if isinstance(child.widget(), QtWidgets.QLineEdit):
                    if action == "connect":
                        child.widget().textChanged.connect(self.documentWasModified)
                    elif action == "save":
                        data.append(child.widget().text())
                    elif action == "load" and data != None:
                        child.widget().setText(data[increment])
                        increment+=1
                if isinstance(child.widget(), QtWidgets.QTextEdit):
                    if action == "connect":
                        child.widget().textChanged.connect(self.documentWasModified)
                    elif action == "save":
                        data.append(child.widget().toPlainText())
                    elif action == "load" and data != None:
                        child.widget().setText(data[increment])
                        increment+=1
                if isinstance(child.widget(), QtWidgets.QTableWidget):
                    if action == "connect":
                        biasX = 0
                        biasY = 0
                        editable = True
                        centered = 2 # центрировать все элементы
                        if child.widget().objectName() in ["tableHours", "tableThemesHoursFooter"]:
                            biasX = 1
                        if child.widget().objectName() == "tableThemesHours":
                            biasY = 3
                            centered = 1 # центрировать все, кроме 1 столбца
                        if child.widget().objectName() == "tableCompetencies":
                            editable = False
                        if child.widget().objectName() == "tableThemes":
                            editable = False
                            centered = 0 # не центрировать элементы
                        if child.widget().objectName() == "tableBrs1":
                            centered = 0
                        for i in range(biasY, child.widget().rowCount()):
                            for j in range(biasX, child.widget().columnCount()):
                                if centered == 0 or (centered == 1 and j == 0):
                                    child.widget().setItem(i, j, self.customQTableWidgetItem(f"", centered = False, editable=editable))
                                else:
                                    child.widget().setItem(i, j, self.customQTableWidgetItem(f"", centered = True, editable=editable))
                        child.widget().itemChanged.connect(self.documentWasModified)
                        child.widget().itemChanged.connect(lambda: self.resizeTables(False))
                        if child.widget().objectName() == "tableThemesHours":
                            child.widget().itemChanged.connect(self.countThemesHours)
                    elif action == "save":
                        biasX = 0
                        biasY = 0
                        if child.widget().objectName() in ["tableHours", "tableThemesHoursFooter"]:
                            biasX = 1
                        if child.widget().objectName() == "tableThemesHours":
                            biasY = 3
                        for i in range(biasY, child.widget().rowCount()):
                            for j in range(biasX, child.widget().columnCount()):
                                data.append(child.widget().item(i, j).text())
                    elif action == "load" and data != None:
                        biasX = 0
                        biasY = 0
                        if child.widget().objectName() in ["tableHours", "tableThemesHoursFooter"]: 
                            biasX = 1
                        if child.widget().objectName() == "tableThemesHours":
                            biasY = 3
                        for i in range(biasY, child.widget().rowCount()):
                            for j in range(biasX, child.widget().columnCount()):   
                                child.widget().item(i, j).setText(f"{data[increment]}")           
                                increment+=1
                if isinstance(child.widget(), QtWidgets.QRadioButton):
                    if action == "connect":
                        child.widget().toggled.connect(self.documentWasModified)
                    elif action == "save":
                        if child.widget().isChecked():
                            data.append(1)
                        else:
                            data.append(0)
                    elif action == "load":
                        if data[increment] == 1:
                            child.widget().setChecked(True)
                        else:
                            child.widget().setChecked(False)
                        increment += 1
                if isinstance(child.widget(), QtWidgets.QComboBox):
                    if action == "connect":
                        child.widget().currentTextChanged.connect(self.documentWasModified)
                        objectName = child.widget().objectName()
                        child.widget().currentTextChanged.connect(lambda: self.comboBoxChanged(objectName))
                        if objectName == "comboBoxFaculty":
                            child.widget().currentTextChanged.connect(lambda: dataBaseModule.updateDepartments(self))
                        elif objectName == "comboBoxDepartment":
                            child.widget().currentTextChanged.connect(lambda: dataBaseModule.updateEmployees(self))
                    elif action == "save":
                        data.append(child.widget().currentText())
                    elif action == "load":
                        child.widget().setCurrentText(data[increment])
                        increment += 1

        if action == "save":
            return data

    def submitThemes(self):
        data = self.textEditThemes.toPlainText().split("\n")
        for i in range(self.tableThemes.rowCount()):
            self.tableThemes.item(i, 0).setText("")
        for i in range(len(data)):
            self.tableThemes.item(i, 0).setText(data[i])
            self.tableThemesHours.item(3+i, 0).setText(data[i])

    def generateThemes(self):
        config = filesModule.loadPreferences()
        options = [config.get('gpt', 'cat-id'), config.get('gpt', 'api-key')]
        data = [self.lineTitle.text()]
        if data == [""]:
            self.openAlert('Сначала укажите наименование дисциплины')
        else:
            request = self.textEditThemes.toPlainText()
            response = requestThemes(data, request, options)
            self.revertBackup = request

            result = ""
            for theme in response.split("\n"):
                if theme == "\n":
                    continue
                theme = theme.replace(":", ".", 1)
                theme = theme.replace("\n", "", 1)
                if re.match("\d.*", theme):
                    theme = "Тема "+ theme
                if not re.match("Тема \d.*", theme):
                    theme = "Тема ?. "+theme
                result = result + theme + "\n"
            self.textEditThemes.setText(result)
    
    def revertThemes(self):
        self.textEditThemes.setText(self.revertBackup)
        self.revertBackup = ""

    def submitThemes2(self):
        data = self.textEditThemes2.toPlainText()
        selected = self.tableThemes.selectedItems()
        if selected and len(selected) == 1:
            selected[0].setText(data)
            self.textEditThemes2.setText("")
            self.revertBackup = ""
            self.lastSelected = ""

    def generateThemes2(self):
        selected = self.tableThemes.selectedItems()
        if selected and len(selected) == 1:
            column_i = selected[0].column()
            row_i = selected[0].row()
            config = filesModule.loadPreferences()
            options = [config.get('gpt', 'cat-id'), config.get('gpt', 'api-key')]
            request = self.textEditThemes2.toPlainText()

            if column_i == 1:
                data = [self.tableThemes.item(row_i, 0).text(), self.lineTitle.text()]
                if data[1] == "":
                    self.openAlert('Сначала укажите наименование дисциплины')
                elif data[0] == "":
                    self.openAlert('Сначала укажите наименование выбранной темы')
                else:
                    response = requestThemeDescription(data, request, options)
                    self.revertBackup = request
                    self.textEditThemes2.setText(response)
            elif column_i == 2:
                data = [self.tableThemes.item(row_i, 0).text(), self.tableThemes.item(row_i, 1).text()]
                if data[0] == "":
                    self.openAlert('Сначала укажите\nнаименование темы')
                elif data[1] == "":
                    self.openAlert('Сначала заполните столбец\n"Описание темы"')
                else:
                    response = requestSeminarQuestions(data, request, options)
                    self.revertBackup = request
                    self.textEditThemes2.setText(response)
            elif column_i == 4:
                data = [self.tableThemes.item(row_i, 0).text(), self.tableThemes.item(row_i, 1).text()]
                if data[0] == "":
                    self.openAlert('Сначала укажите\nнаименование темы')
                elif data[1] == "":
                    self.openAlert('Сначала заполните столбец\n"Описание темы"')
                else:
                    response = requestHomeworkQuestions(data, request, options)
                    self.revertBackup = request
                    self.textEditThemes2.setText(response)
            else:
                self.openAlert("Для этого столбца нельзя запросить помощь ассистента")

    def revertThemes2(self):
        self.textEditThemes2.setText(self.revertBackup)
        self.revertBackup = ""

    def submitCompetencies(self):
        data = self.textEditComp.toPlainText()
        selected = self.tableCompetencies.selectedItems()
        if selected and len(selected) == 1:
            selected[0].setText(data)
            self.textEditComp.setText("")
            self.revertBackup = ""
            self.lastSelected = ""

    def generateCompetencies(self):
        selected = self.tableCompetencies.selectedItems()
        if selected and len(selected) == 1:
            column_i = selected[0].column()
            row_i = selected[0].row()
            config = filesModule.loadPreferences()
            options = [config.get('gpt', 'cat-id'), config.get('gpt', 'api-key')]
            request = self.textEditComp.toPlainText()
            
            if column_i == 1:
                self.openAlert("Для этого столбца нельзя запросить помощь ассистента")
            elif column_i == 2:
                data = [self.tableCompetencies.item(row_i, 1).text()]
                if data == [""]:
                    self.openAlert('Сначала заполните столбец "Наименование компетенции"')
                else:
                    response = requestCompetenciesIndicators(data, request, options)
                    self.revertBackup = request
                    self.textEditComp.setText(response)
            elif column_i == 3:
                data = [self.lineTitle.text(), self.tableCompetencies.item(row_i, 1).text(), self.tableCompetencies.item(row_i, 2).text()]
                if data[0] == "":
                    self.openAlert('Сначала укажите наименование дисциплины')
                elif data[1] == "":
                    self.openAlert('Сначала заполните столбец "Наименование компетенции"')
                elif data[2] == "":
                    self.openAlert('Сначала заполните "Индикаторы достижения компетенции"')
                else:
                    response = requestCompetenciesResults(data, request, options)
                    self.revertBackup = request
                    self.textEditComp.setText(response)
                
    def revertCompetencies(self):
        self.textEditComp.setText(self.revertBackup)
        self.revertBackup = ""

    def generateThemesHours(self):
        config = filesModule.loadPreferences()
        options = [config.get('gpt', 'cat-id'), config.get('gpt', 'api-key')]
        request = None

        if len([1 for i in range(3, self.tableThemesHours.rowCount()) if self.tableThemesHours.item(i, 0).text() != ""]) < 1:
            self.openAlert('Сначала распределите\nтемы')
        else:
            data = [self.textEditThemes.toPlainText(), f"Лекции: {self.tableThemesHoursFooter.item(0, 3).text()} часов, семинары: {self.tableThemesHoursFooter.item(0, 4).text()} часов, самостоятельная работа: {self.tableThemesHoursFooter.item(0, 5).text()} часов."]
            response = requestHintThemesHours(data, request, options)
            self.hint.textBrowserAI.setText(response)
            self.hint.show()

    def fillEvenlyThemesHours(self):
        cThemes = 0
        for i in range(3, self.tableThemesHours.rowCount()):
            if self.tableThemesHours.item(i, 0).text() != "":
                cThemes += 1
        if cThemes == 0:
            self.openAlert("Сначала распределите\nтемы")
        else:
            for i in range(3):
                element = self.tableThemesHoursFooter.item(0, i+3)
                if element.text().isdigit():
                    average = int(element.text()) / cThemes
                    for j in range(3, self.tableThemesHours.rowCount()):
                        if self.tableThemesHours.item(j, 0).text() != "":
                            self.tableThemesHours.item(j, i+3).setText(str(floor(average)))
                            if j < 29 and self.tableThemesHours.item(j+1, 0).text() == "":
                                self.tableThemesHours.item(j, i+3).setText(str(int(element.text()) - (cThemes-1) * floor(average)))            

    def countThemesHours(self):
        sums = [0, 0, 0, 0, 0]
        for i in range(3, self.tableThemesHours.rowCount()):
            total = self.tableThemesHours.item(i, 1)
            aud = self.tableThemesHours.item(i, 2)
            lec = self.tableThemesHours.item(i, 3)
            sem = self.tableThemesHours.item(i, 4)
            sam = self.tableThemesHours.item(i, 5)
            if lec.text() != "" and sem.text() != "":
                aud.setText(str(int(lec.text()) + int (sem.text())))
            if aud.text() != "" and sam.text() != "":
                total.setText(str(int(aud.text()) + int (sam.text())))
            for j in range(0, 5):
                element = self.tableThemesHours.item(i, j+1)
                if element.text().isdigit():
                    sums[j] += int(element.text())

        for i in range(len(sums)):
            element = self.tableThemesHoursFooter.item(0, i+1)
            if element.text().isdigit() and sums[i] == int(element.text()):
                element.setBackground(QtGui.QColor(144,238,144))
            else:
                element.setBackground(QtGui.QColor(255,255,255))

    def documentWasModified(self):
        self.setWindowModified(True)

    def comboBoxChanged(self, widget):
        if widget == "comboBoxFormat":
            if self.comboBoxFormat.currentText() == ".pdf":
                self.lineFilePath.setText(self.lineFilePath.text().replace('.docx', '.pdf'))
            else:
                self.lineFilePath.setText(self.lineFilePath.text().replace('.pdf', '.docx'))

    def customQTableWidgetItem(self, caption, centered = True, editable = True):
        item = QTableWidgetItem(caption)
        if centered:
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        if not editable:
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        return item
    
    def resizeTables(self, first = False):
        self.tableHours.resizeRowsToContents()
        self.tableHours.resizeColumnsToContents()
        if first:
            self.tableThemes.resizeRowsToContents()
            self.tableThemes.resizeColumnsToContents()
    
    def setFontSize(self):
        config = filesModule.loadPreferences()
        fs = config.get("main", "font-size")
        self.setFont(QFont('Times', int(fs)))
        self.preferences.setFont(QFont('Times', int(fs)))
        self.hint.setFont(QFont('Times', int(fs)))
        self.alert.setFont(QFont('Times', int(fs)))

    def doubleClickThemes(self, _):
        if self.lastSelected != "": 
            self.lastSelected.setText(self.textEditThemes2.toPlainText())
        selected = self.tableThemes.selectedItems()
        if len(selected) == 1:
            self.textEditThemes2.setText(selected[0].text())
            self.revertBackup = ""
            self.lastSelected = selected[0]

    def doubleClickCompetencies(self, _):
        if self.lastSelected != "":
            self.lastSelected.setText(self.textEditComp.toPlainText())
        selected = self.tableCompetencies.selectedItems()
        if len(selected) == 1:
            self.textEditComp.setText(selected[0].text())
            self.revertBackup = ""
            self.lastSelected = selected[0]

if __name__ == '__main__':
    app = QApplication(sys.argv)  
    window = RpdWindow() 
    window.show()  
    app.exec_()