from configparser import ConfigParser
import os
import json

def loadPreferences():
    config = ConfigParser()
    config.read('config.ini')
    if config.read("config.ini") == []:
        config.clear()
        config.add_section('main')
        config.add_section('gpt')
        config.set('main', 'font-size', '10')
        config.set('gpt', 'cat-id', '')
        config.set('gpt', 'api-key', '')
        with open('config.ini', 'w') as f:
            config.write(f)
    return config

def chooseExportPath(window, fileDialog, document="rpd"):
    if document == "rpd":
        fileName, _ = fileDialog.getSaveFileName(window, "Save File", "", "All Files(*);;Word (*.docx);;PDF (*.pdf)")
        if fileName:
            if window.comboBoxFormat.currentText() == ".pdf":
                fileName = fileName.replace('.docx', '.pdf')
            else:
                fileName = fileName.replace('.pdf', '.docx')
                window.lineFilePath.setText(fileName)
    elif document == "brs":
        fileName, _ = fileDialog.getSaveFileName(window, "Save File", "", "All Files(*);;Word (*.docx)")
        if fileName:
            window.lineFilePath2.setText(fileName)

        

def saveFile(window, fileDialog):
    if not window.isWindowModified():
        return
    if not window.fileName:
        saveAsFile(window, fileDialog)
    else:
        data = window.manageFields("save")
        with open(window.fileName, 'w', encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
        window.setWindowModified(False)

def saveAsFile(window, fileDialog, erase=False):
    fileName, _ = fileDialog.getSaveFileName(window, 
        "Save File", "", "Json Files(*.json)")
    if fileName:
        if erase:
            window.manageFields("load", ["" for i in range(1500)])
        data = window.manageFields("save")
        with open(fileName, 'w', encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
        window.fileName = fileName
        window.setWindowTitle(str(os.path.basename(fileName)) + f" - {window.windowTitle}")
        window.setWindowModified(False)
    
def openFile(window, fileDialog):
    fileName, _ = fileDialog.getOpenFileName(window,
        "Load File", "", "Json Files(*.json)")
    if fileName:
        data = []
        with open(fileName, "r", encoding="utf8") as f:
            data = json.load(f)
        window.manageFields("load", data)
        window.fileName = fileName
        window.setWindowTitle(str(os.path.basename(fileName)) + " - РПД Менеджер[*]")
        window.setWindowModified(False)
        window.lastSelected = ""
    
def newFile(window, fileDialog):
    window.setWindowModified(False)
    saveAsFile(window, fileDialog, erase=True)
    window.lastSelected = ""

def closeFile(window):
    window.manageFields("load", ["" for i in range(1500)])
    window.setWindowTitle(window.windowTitle)
    window.setWindowModified(False)
    window.lastSelected = ""