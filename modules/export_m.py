from docxtpl import DocxTemplate
import re
from datetime import datetime
from docx2pdf import convert
import os

def exportFileRpd(filePath, data, formating = True, format = 'docx'):
    if formating:
        doc = DocxTemplate(f"templates/full.docx")
    else:
        doc = DocxTemplate(f"templates/simple.docx")
    context = processData(data)
    doc.render(context)
    doc.save(filePath.replace(".pdf", ".docx"))
    if format == 'pdf':      
        convert(filePath.replace(".pdf", ".docx"), filePath.replace(".docx", ".pdf"))
        os.remove(filePath.replace(".pdf", ".docx"))

def exportFileBrs(filePath, data):
    doc = DocxTemplate(f"templates/brs.docx")
    context = processData2(data)
    doc.render(context)
    doc.save(filePath)

def themesPunct(theme):
    # theme = theme.replace(":", ".", 1)
    if not re.match("Тема \d.*", theme):
        theme = "Тема ?. "+theme
    return theme

def themesDescTabulation(desc):
    if not "\t" in desc and "\n" in desc:
        strings = desc.split("\n")
        for i in range(len(strings)):
            strings[i] = f"\t{strings[i]}"
        desc = "\n".join(strings)
    return desc

def processData(data):
    context = {}
    context["year"] = datetime.now().year
    context["title"] = data[0]
    context["faculty"] = data[66]
    context["department"] = data[67]
    context["dot"] = data[2]
    context["compilers"] = data[68]
    context["reviewers"] = data[69]
    context["place"] = data[1]

    col_labels = ["Всего (в з/е и в часах)", "Семестр 1 (в часах)", "Семестр 2 (в часах)", "Семестр 3 (в часах)", "Семестр 4 (в часах)",
                  "Семестр 5 (в часах)", "Семестр 6 (в часах)", "Семестр 7 (в часах)", "Семестр 8 (в часах)"]
    context["table_hours"] = {
        'col_labels': [col_labels[i] for i in range(len(col_labels)) if data[3+i] != ''],
        'rows1': [
            {'label': 'Общая трудоемкость дисциплины', 'cols': [e for e in data[3:12] if e!='']},
            {'label': 'Контактная работа - аудиторные занятия', 'cols': [e for e in data[12:21] if e!='']},
            {'label': 'Лекции', 'cols': [e for e in data[21:30] if e!='']},
            {'label': 'Семинары, практически занятия', 'cols': [e for e in data[30:39] if e!='']},
            {'label': 'Самостоятельная работа', 'cols': [e for e in data[39:48] if e!='']},
        ],
        'rows2': [
            {'label': 'Вид текущего контроля', 'cols': [e for e in data[49:57] if e!='']},
            {'label': 'Вид промежуточной аттестации', 'cols': [e for e in data[58:66] if e!='']}

        ]
    }

    context["table_competencies"] = {
        'col_labels': ['Код компетенции', 'Наименование компетенции', 'Индикаторы достижения компетенции', 'Результаты обучения (умения и знания), соотнесенные с индикаторами достижения компетенции'],
        'rows': [{'cols': [data[i], data[i+1], data[i+2], data[i+3]]} for i in range(70, 130, 4) if data[i] != '']# rowsCompetencies,
    }

    context["themes"] = [{'name': data[i], 'description': themesDescTabulation(data[i+1])} for i in range(133, 312, 6) if data[i] != ""]

    rowsThemesHours = []
    increment = 0
    for i in range(313, 523, 7):
        if data[i] != '':
            increment += 1
            rowsThemesHours.append({'i': increment,'name': ". ".join(themesPunct(data[i]).split(". ")[1:]), 'all': data[i+1], 'aud': data[i+2], 'lec': data[i+3], 'sem': data[i+4], 'sam': data[i+5], 'cc': data[i+6]})
    context["table_themes_hours"] = {
        'rows': rowsThemesHours,
    }
    context["tf"] = {
        'all': data[523], 'aud': data[524], 'lec': data[525], 'sem': data[526], 'sam': data[527], 'cc': data[528],
                          'audp': data[530], 'lecp': data[531], 'semp': data[532], 'samp': data[533]
    }

    context["sems"] = {
        'col_labels': ['Наименование тем (разделов) дисциплины', 'Перечень вопросов для обсуждения на семинарских, практических занятиях, рекомендуемые источники из разделов 8,9 (указывается раздел и порядковый номер источника)', 'Формы проведения занятий'],
        'rows': [{'cols': [themesPunct(data[i])[5:], data[i+2], data[i+3]]} for i in range(133, 313, 6) if data[i] != '']
    }
    context["sams"] = {
        'col_labels': ['Наименование тем (разделов) дисциплины', 'Перечень вопросов, отводимых на самостоятельное освоение', 'Формы внеаудиторной самостоятельной работы'],
        'rows': [{'cols': [themesPunct(data[i])[5:], data[i+4], data[i+5]]} for i in range(133, 313, 6) if data[i] != '']
    }
    context["kr_qz"] = data[1095]
    context["table_dost_comp"] = {
        'col_labels': ['Наименование компетенции', 'Индикаторы достижения компетенции', 'Результаты обучения (умения и знания), соотнесенные с индикаторами достижения компетенции', 'Типовые контрольные задания'],
        'rows': [{'cols': [data[i], data[i+1], data[i+2], data[1097+(i-70)//2]]} for i in range(70, 130, 4) if data[i] != '']
    }

    context["exam_q"] = data[1127]
    context["exam_z"] = data[1126]
    context["literature"] = data[1128]
    context["resources"] = data[1129]
    context["method"] = data[1130]
    context["lic"] = data[1131]
    context["bd"] = data[1132]
    context["apparat"] = data[1133]
    context["math_tech"] = data[1134]

    return context

def processData2(data):
    context = {}
    context["title"] = data[0]
    context["dot"] = data[2]
    context["table_brs"] = {
        'col_labels': ['№ п/п', 'Вид отчетности', 'Баллы', 'Максимальные баллы'],
        'rows': [{'cols': [data[i], data[i+1], data[i+2], data[i+3]]} for i in range(1139, 1258, 4) if data[i] != '']
    }
    return context