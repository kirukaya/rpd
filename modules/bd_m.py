import sqlite3

def getFaculties(window):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM faculties''')
    faculties = cursor.fetchall()
    for faculty in faculties:
        window.comboBoxFaculty.addItem(faculty[0])

    window.comboBoxFaculty.setCurrentText("")
    connection.close()

def updateDepartments(window):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    currentFaculty = window.comboBoxFaculty.currentText()
    cursor.execute('''SELECT id FROM faculties WHERE name = ?''', (currentFaculty,))
    result = cursor.fetchall()
    if result != []:
        window.comboBoxDepartment.clear()
        cursor.execute('''SELECT name FROM departments WHERE faculty_id = ?''', (result[0][0],))
        departments = cursor.fetchall()
        for department in departments:
            window.comboBoxDepartment.addItem(department[0])
    connection.close()

def updateEmployees(window):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    currentDepartment = window.comboBoxDepartment.currentText()
    cursor.execute('''SELECT id FROM departments WHERE name = ?''', (currentDepartment,))
    result = cursor.fetchall()
    if result != []:
        window.comboBoxCompiler.clear()
        window.comboBoxReviewer.clear()
        cursor.execute('''SELECT name FROM employees WHERE department_id = ? OR department_id = ?''', (result[0][0], 57,))
        departments = cursor.fetchall()
        for department in departments:
            window.comboBoxCompiler.addItem(department[0])
            window.comboBoxReviewer.addItem(department[0])
    connection.close()

def getCompetencies():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT code, definition FROM competencies''')
    results = cursor.fetchall() 
    connection.close()
    return results