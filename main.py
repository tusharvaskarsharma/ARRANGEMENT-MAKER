import csv
import datetime
import pandas
import random
import pickle

# TO OPEN THE CORRECT FILE OF THAT DAY
def day():
    today_date = datetime.date.today()
    daw = today_date.strftime("%A")
    return daw + '.csv'

# TO FETCH ALL THE TEACHER
all_teacher_list = []
temp_list = []
def all_teacher(f):
    global all_teacher_list
    with open(f) as ifile:
        csvr = csv.reader(ifile)
        next(ifile)
        for row in csvr:
            all_teacher_list.append(row)
            temp_list.append(row)


def remove_absent_teacher(lst):
    for teacher in lst:
        for lst_teacher in all_teacher_list:
            if lst_teacher[0] == teacher:
                all_teacher_list.remove(lst_teacher)