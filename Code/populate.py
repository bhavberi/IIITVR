import csv
import pymysql
import os
import sys


def read_csv(filename):
    rows = []
    filename = "./CSVs/"+filename+".csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)

    return rows, fields


def insert(table, format):

    rows, fields = read_csv(table)
    fields = ", ".join(fields)

    if fields != "":
        command = 'insert into {}({}) values ({})'.format(
            table, fields, format)
    else:
        command = 'insert into {} values ({})'.format(
            table, format)

    for row in rows:
        try:
            cur_obj.execute(command.format(*row))
        except Exception as e:
            print(e)

    print("Done inserting values for %s table" % (table))


try:
    pymysql_obj = pymysql.connect(host="localhost", port=3306, user="hp", password=str(
        os.environ["MYSQL_PASS"]), database="dna_project_team1", autocommit=True)
    cur_obj = pymysql_obj.cursor(pymysql.cursors.DictCursor)
except Exception as e:
    print(e)
    exit(0)

# EMPLOYEES
name = "Employees"
fields = "Employee_Name, Department, Supervisor_ID"
format = "'{}', '{}', {}"
insert(name, format)

# PLANS
name = "Plans"
fields = "Cost, Duration"
format = "{}, {}"
insert(name, format)

# Plans_Features
name = "Plans_Features"
fields = ""
format = "{}, '{}'"
insert(name, format)

# User
name = "User"
fields = "Aadhar_Number,Name,Gender,DOB,Joining_Date,Plan_ID"
format = "{},'{}', '{}', '{}', '{}', {}"
insert(name, format)

# Chats
name = "Chats"
fields = ""
format = "{}, {}, '{}', '{}'"
insert(name, format)

# Issues
name = "Issues"
format = "'{}', {},{},{},'{}'"
insert(name, format)

# MetaReality
name = "MetaReality"
format = "'{}', '{}', '{}'"
insert(name, format)

# Preferences
name = "Preferences"
format = "{}, {}, '{}', '{}'"
insert(name, format)

# Preferance_Language
name = "Preferance_Language"
format = "{}, '{}'"
insert(name, format)

# Preferance_Language
name = "Preferance_Country"
format = "{}, '{}'"
insert(name, format)

# Makes
name = "Makes"
format = "{}, {}, {}"
insert(name, format)

# Maintains
name = "Maintains"
format = "'{}', {}, {}"
insert(name, format)

# Photos
table = "Photos"
rows, fields = read_csv(table)

command = "insert into {} values ({})".format(
    table, '{}, "{}",{},"{}"')

for row in rows:
    blob = ""
    try:
        fp = open(row[2], "rb")
        blob = fp.read()
    except Exception as e:
        print(e)
        continue

    try:
        cur_obj.execute(command.format(row[0], row[1], str(
            os.path.getsize(row[2])), blob.hex()))
    except Exception as e:
        print(e)

print("Done inserting values for %s table" % (table))
