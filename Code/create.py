import pymysql
import os

try:
    pymysql_obj = pymysql.connect(host="localhost", port=3306, user="hp", password=str(
        os.environ["MYSQL_PASS"]), autocommit=True)
except Exception as e:
    print(e)
    exit(1)

pymysql_obj.cursor().execute("DROP DATABASE IF EXISTS dna_project_team1")
pymysql_obj.cursor().execute("CREATE DATABASE dna_project_team1")
pymysql_obj.close()

try:
    pymysql_obj = pymysql.connect(host="localhost", port=3306, user="hp", password=str(
        os.environ["MYSQL_PASS"]), database="dna_project_team1", autocommit=True)
except Exception as e:
    print(e)
    exit(1)

sqlCommands = list()
try:
    fd = open('tables.sql', 'r')
    sqlFile = fd.read()
    fd.close()

    # Remove the last empty entry coming due to split function
    sqlCommands = sqlFile.split(';')[:-1]
except Exception as e:
    print(e)
    exit(0)

cur_obj = pymysql_obj.cursor()

# Execute every command from the input file
for command in sqlCommands:
    try:
        cur_obj.execute(command)
    except Exception as e:
        print(command)
        print("Command skipped -> ", e)

print("Done creating the tables")

cur_obj.close()
pymysql_obj.close()
