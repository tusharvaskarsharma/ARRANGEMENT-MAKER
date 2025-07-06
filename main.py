"""
This program is designed to generate timetable arrangements for a school 
in the event of teacher absences.

Workflow:
1. Data Preparation:
   - Each day's teacher timetable is stored in a separate CSV file named 
     after the day (e.g., Monday.csv, Tuesday.csv, etc.).

2. Identifying the Current Day:
   - The function `day()` uses the datetime module to determine the 
     current day of the week and selects the corresponding timetable CSV 
     file for processing.

3. Loading the Timetable:
   - The function `list_all_teacher(f)` reads the day-specific CSV file 
     and converts it into a list of lists named `all_teacher_list`. 
     Each sub-list represents a teacher’s timetable for that day.

4. Managing Present and Absent Teachers:
   - The list `pre_teacher_list` stores the names of teachers who are 
     present on that day.
   - The function `list_of_teacher_menu()` displays a menu listing all 
     teachers’ names and prompts the user to input the names of absent 
     teachers as a list.

5. Processing Absent Teachers:
   - The function `ab_pre_teacher_list(lst)` processes the list of 
     absent teachers and generates:
        - A dictionary containing the names of present teachers along 
          with their assigned periods.
        - A separate dictionary for absent teachers, mapping each absent 
          teacher’s name to the list of periods they were scheduled to 
          teach.

Using this information, the program facilitates the reassignment of 
periods initially allocated to absent teachers, thereby maintaining a 
functional timetable for the school day.
"""


import csv # for reading csv file and writing in an ARRANGEMENT.CSV file
import datetime # for selecting the day and for recording the data in server
import math # math module is for the rounding off the average class of teachers
import random # for randomly selecting the teacher from the available teachers
import tabulate # for printing in a tabulate format
import mysql.connector as myc # for connecting the python to sql server for recording the absent teachers data

# Global variables
all_teacher_list = []  # This list stores the complete timetable data for all teachers on the current day.
pre_teacher_list = []  # This list contains the names of teachers who are present on the current day.


'''=================================================================================================================='''
"""
The `day` function determines which file to load based on the current day.
Each day has a separate CSV file, and this function identifies which file 
should be used for processing on the current date.
"""
def day():
    today_date = datetime.date.today()
    dayy = today_date.strftime("%A")
    return dayy + '.csv' # returns the file name according to the day


'''=================================================================================================================='''
"""
This represents a list of lists containing the timetable details 
for all teachers on the current day.
"""
def list_all_teacher(f): # function will read all the lines in the file
    try:
        ifile = open(f, 'r')
        csv_read = csv.reader(ifile)
        next(csv_read)
        for row in csv_read:
            all_teacher_list.append(row)
            pre_teacher_list.append(row)
        ifile.close()
    except FileNotFoundError:
        print(f"File {f} not found. Please check the file name and try again.")
        exit(1)
    except Exception as e:
        print(f"Error reading file {f}: {e}")
        exit(1)


'''=================================================================================================================='''
"""
This generates separate lists of absent and present teachers 
from the main list of all teachers.
"""
ab_teacher_dict = {} # this the dictionay for the absent teacher periods

def ab_pre_teacher_list(lst):
    # This function identifies absent and present teachers 
    # based on the provided list of absent teacher names.
    for i in lst:
        for row in all_teacher_list:
            if i == row[0]:
                t_lst = []
                for ele in range(1, 9):
                    if row[ele] != '':
                        t_lst.append(ele)
                ab_teacher_dict[row[0]] = t_lst
                pre_teacher_list.remove(row) # removing abesnt teachers from all teacher list


'''=================================================================================================================='''
"""
This creates a menu listing all teachers, from which the user 
can select the names of the teachers who are absent.
"""
def list_of_teacher_menu(): 
    # it will give a menu type attendance sheet to easy mark attendance
    ab_tea_name_list = [] # list of absent teacher names
    count = 0
    for i in all_teacher_list:
        count += 1
        print(count, '. ', i[0]) # print the menu of teachers
    try:
        ab_teacher_input = input("Enter the serial numbers of absent teachers, separated by commas: ")
        ab_teacher = [int(x.strip()) for x in ab_teacher_input.split(',') if x.strip().isdigit()]
    except Exception as e:
        print("Invalid input. Please enter numbers separated by commas.")
        return list_of_teacher_menu()
    for j in ab_teacher:
        if 1 <= j <= len(all_teacher_list):
            ab_tea_name_list.append(all_teacher_list[j - 1][0])
        else:
            print(f"Serial number {j} is out of range.")
    return ab_tea_name_list


'''=================================================================================================================='''


def average_class_day(free_lst):
    # The argument 'free_lst' is a list of lists, where each sub-list 
    # contains the names of teachers available during a specific period 
    # for substituting an absent teacher.
    change_pre_teacher_list = pre_teacher_list[:] 
    # Creates a copy of the present teachers list so that it can be 
    # modified during the arrangement process without altering 
    # the original list.
    arrang_teacher_list = []
    count = 0
    for j in all_teacher_list:
        for i in j[1:]:
            if i != '':
                count += 1
    avg_class = math.ceil(count / len(change_pre_teacher_list)) # for rounding off the average class value
    for i in free_lst:
        # This loop filters out the teachers who have fewer periods 
        # than the average for that day, to ensure fair distribution 
        # of substitution duties.
        temp_teacher_list = []
        # A temporary list to store the names of teachers whose total 
        # number of classes for the day is less than the average.
        for k in i:
            for j in change_pre_teacher_list:
                c = 0
                if k == j[0]:
                    for h in j[1:]:
                        if h != '':
                            c += 1
                    if c <= avg_class:
                        temp_teacher_list.append(j[0]) # The teacher meeting the condition is added to this list.
        arrang_teacher_list.append(temp_teacher_list)
    return arrang_teacher_list


'''=================================================================================================================='''
arrangement_list = [] # THIS LIST WILL STORE THE ARRANGEMENT OF TEACHERS FOR THE DAY ( MAIN ARRANGEMENT LIST )


def arrangement_maker(tec, per): # tec --> teacher name , per --> there period list
    change_pre_teacher_list = pre_teacher_list[:] #     
    # This creates a copy of the list of present teachers 
    # to allow modifications without altering the original list.
    free_teacher = []
    for p in per:
        st = []
        for pe in pre_teacher_list:
            if pe[p] == '':
                st.append(pe[0])
        free_teacher.append(st)
    for i in all_teacher_list:
        if i[0] == tec:
            teacher_routine = i[1:]
    local_arrangement = []   # This list stores the local arrangement details for the current period.
    local_arrangement.append(tec)   # Adds the name of the teacher who has been assigned to cover the arrangement.
    for period in range(0,8): # for 0 to 8 period as for of an element ho list
        arrangement_teacher = average_class_day(free_teacher)
        # This function is called to get a list of teachers available
        if teacher_routine[period] != '':
        # If the teacher does not have a free period at this time,
        # then an arrangement needs to be made.
            for k in arrangement_teacher:
                ran_teacher = random.choice(k) # This selects a random teacher from the list of available (free) teachers.
                line = str(ran_teacher) + " in " + str(teacher_routine[period])
                local_arrangement.append(line)
                for t in change_pre_teacher_list:
                    # This loop updates the list of present teachers after an arrangement 
                    # has been assigned, to reflect the new teaching load.
                    if t[0] == ran_teacher:
                        t[period+1] = line
                        # Updates the period in the teacher's schedule with the arrangement.
                break
        else:
            local_arrangement.append('')
    arrangement_list.append(local_arrangement) # And this stores the arrangements for all teachers in a single list.



'''=================================================================================================================='''

def printing_arrangement(): # prints and saves arrangement
    try:
        ofile = open("ARRANGEMENT.CSV", 'w', newline='')
        csvw = csv.writer(ofile)
        csvw.writerow(['TEACHERS', 1, 2, 3, 4, 5, 6, 7, 8])
        for TEACHER in arrangement_list:
            csvw.writerow(TEACHER)
        ofile.close()
        head = ["TEACHER", "1ST", "2ND", "3RD", "4TH", "5TH", "6TH", "7TH", "8TH"]
        arrang_tale = tabulate.tabulate(arrangement_list, headers=head, tablefmt="grid")
        print(arrang_tale)
    except Exception as e:
        print(f"Error writing arrangement: {e}")


if __name__ == '__main__': # main calling area
    file_name = day()
    file_name = "Monday.csv"  # Use correct case
    list_all_teacher(file_name)
    ab_teacher_name = list_of_teacher_menu()
    ab_pre_teacher_list(ab_teacher_name)
    for key, val in ab_teacher_dict.items():
        arrangement_maker(key, val)
    printing_arrangement()



