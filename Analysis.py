import sqlite3
import openpyxl


def analysis(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Counting attending classes
    cursor.execute("SELECT * FROM absents")

    results = cursor.fetchall()
    # print(results)
    # print(type(results))
    plus = 0
    minus = 0
    groupVisitationDict = {}
    for tuple in results:
        for el in tuple:
            if el == '+':
                plus += 1
            elif el == '-':
                minus += 1
        groupVisitationDict.update({tuple[0]: {'+': plus, '-': minus}})
        minus = 0
        plus = 0

    # print(groupVisitationDict);
    # End counting attending classes

    # Count of qustions
    cursor.execute("select COUNT(*) from asks")
    results = cursor.fetchall()
    countOfQuestions = results[0][0]
    # print(countOfQuestions);
    # End count of questions

    # Homework
    cursor.execute("SELECT Count(*) FROM homeworks")

    results = cursor.fetchall()
    countOfTasks = results[0][0]
    # print(countOfTasks);
    # End of Homework

    # Count of Students
    cursor.execute("SELECT * FROM students")

    results = cursor.fetchall()

    studFIO = ''
    studentsDict = {}
    for tup in results:
        for i in range(1, len(tup)):
            studFIO += tup[i] + ' '
        studentsDict.update({tup[0]: studFIO})
        studFIO = ''

    # print(studentsDict)
    # End count of students

    # EXCEL writing
    f_name = 'analysis.xlsx'
    wb = openpyxl.Workbook()
    # ws = wb.active;
    sheet = wb._sheets[0]
    # ws.merge_cells['A1:B1']
    sheet['A1'] = 'Количество активных вопросов:'
    sheet['A2'] = countOfQuestions

    sheet['c1'] = 'Количество активных заданий:'
    sheet['c2'] = countOfTasks

    sheet['E1'] = 'Количество студентов на курсе:'
    k = 2
    for i in studentsDict:
        sheet['E' + str(k)] = i
        sheet['F' + str(k)] = studentsDict[i]
        k += 1

    k = 2
    # print(groupVisitationDict)
    sheet['H1'] = 'Прогулы курса:'
    for i in groupVisitationDict:
        sheet['H' + str(k)] = i
        for j in groupVisitationDict[i]:
            if j == '+':
                sheet['I' + str(k)] = j
                sheet['J' + str(k)] = groupVisitationDict[i][j]
            elif j == '-':
                sheet['K' + str(k)] = j
                sheet['L' + str(k)] = groupVisitationDict[i][j]
        k += 1

    wb.save(f_name)

    # End EXCEL writing

    conn.close()
    return f_name
