import pymysql
import os
from prettytable import from_db_cursor
from subprocess import call


def clear():
    x = call('clear' if os.name == 'posix' else 'cls')


"""
FUNCTIONS DEFINITIONS STARTS
"""

# ADMIN
def raw_sql():
    print("Enter/Paste your command. Ctrl-D or Ctrl-Z ( windows ) to execute it.")

    command = ""
    while True:
        try:
            line = input()
        except EOFError:
            break
        command += " "
        command += line

    command.strip(";")

    try:
        print(cur_obj.execute(command))
    except Exception as e:
        print(e)


# PUBLIC
def new_user():
    print("Enter User's Details")
    name = input("Name: ")
    aadhar = input("Aadhar Number: ")
    Gender = input("Gender (M/F/O): ")
    print("DOB (For Age Verification Purposes) - Format 'YYYY-MM-DD'")
    DOB = input(":")

    command = 'INSERT INTO User(Name,Aadhar_Number,Gender,DOB) VALUES ("{}",{},"{}","{}")'
    try:
        cur_obj.execute(command.format(name, aadhar, Gender, DOB))
    except Exception as e:
        print(e)

    id = 0
    command = "SELECT User_ID from User where Aadhar_Number = {}".format(
        aadhar)
    try:
        cur_obj.execute(command)
        id = cur_obj.fetchone()[0]
    except Exception as e:
        print(e)

    print("User created successfully with ID = {}".format(id))
    print("Store it for future uses")
    return id

# USER
def delete_user():
    sure = input("Input Y/y to continue. -> ")
    if sure.lower() == "y":
        command = 'DELETE FROM User where User_id={}'
        try:
            cur_obj.execute(command.format(user_id))
        except Exception as e:
            print(e)

# EMPLOYEE
def leave_company():
    sure = input("Input Y/y to continue. -> ")
    if sure.lower() == "y":
        command = 'DELETE FROM Employee where Employee_ID={}'
        try:
            cur_obj.execute(command.format(emp_id))
        except Exception as e:
            print(e)

# USER
def send_chat():
    receiver = input("Enter Reciver User ID: ")
    content = input("Enter your message\n:")
    if(len(content) > 499):
        print("Sorry we don't support this long messages. Max len = 500 chars")
        content = input("Enter your issue: ")
        if(len(content) > 499):
            print("TOO LONG MSG AGAIN")
            return

    command = 'INSERT INTO Chats(Sender,Receiver,Content) VALUES ({},{},"{}")'
    try:
        cur_obj.execute(command.format(user_id, receiver, content))
    except Exception as e:
        print(e)

# USER
def new_issue():
    content = input("Enter your Issue\n:")
    if(len(content) > 499):
        print("Sorry we don't support this long messages. Max len = 500 chars")
        content = input("Enter your issue: ")
        if(len(content) > 499):
            print("TOO LONG MSG AGAIN")
            return

    command = 'INSERT INTO Issues(User_ID,Content) VALUES ({},"{}")'
    try:
        cur_obj.execute(command.format(user_id, content))
    except Exception as e:
        print(e)

# EMPLOYEE
def resolve_issue():
    id = input("Enter Issue ID: ")

    command = 'UPDATE Issues SET Resolved=true, Employee_ID={} where Issue_ID = {}'
    try:
        cur_obj.execute(command.format(emp_id, id))
    except Exception as e:
        print(e)

# User, Employee
def show_plan():
    command = 'SELECT a.*,b.Features FROM Plans a join Plans_Features b  on a.Plan_ID=b.Plan_ID'
    try:
        cur_obj.execute(command)
        plans = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(plans)

# User
def change_plan():
    plan = input("Enter Plan ID: ")
    command = 'UPDATE User SET Plan_ID={} where User_ID={}'
    try:
        cur_obj.execute(command.format(plan, user_id))
    except Exception as e:
        print(e)

# EMPLOYEE
def update_plan():
    plan = input("Enter Plan ID: ")
    cost = input("Enter Updated plan Cost: ")
    Duration = input("Enter Updated Plan Duration (In no of Days): ")

    command = 'UPDATE Plans SET Cost={}, Duration={} where Plan_ID={}'
    try:
        cur_obj.execute(command.format(cost, Duration, plan))
    except Exception as e:
        print(e)

# EMPLOYEE
def new_plan():
    id = 0
    cost = input("Enter the cost of the new plan: ")
    Duration = input("Enter Plan Duration (In no of Days): ")

    command = 'INSERT INTO Plans (Cost, Duration) values ({:.2f},{})'

    try:
        cur_obj.execute(command.format(cost, Duration))
        cur_obj.execute("SELECT LAST_INSERT_ID()")
        id = cur_obj.fetchone()
    except Exception as e:
        print(e)
        return 
    
    print("Keep on entering the features of the plan. When there are no more, enter -1")
    while 1:
        i = input("> ")
        if i=="-1":
            return
        
        if len(i) > 99:
            print("Long Messages not supported.")
            continue
        
        command = 'INSERT INTO Plans_Features (Plan_ID, Features) values ({},"{}")'
        try:
            cur_obj.execute(command.format(id, i))
        except Exception as e:
            print(e)
            return

# EMPLOYEE
def old_new_user():
    command = '(select * from User order by DOB,User_ID limit 1) union (select * from User order by DOB desc,User_ID limit 1)'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# EMPLOYEE
def premium_users():
    command = 'select User_ID, Name, Gender, a.Plan_ID from User a join Plans b on a.Plan_ID = b.Plan_ID where Cost > (select AVG(Cost) from Plans)'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# EMPLOYEE
def user_high_low_plan():
    command = 'select User_ID, Name, Joining_Date from User join Plans on User.Plan_ID = Plans.Plan_ID where Plans.Cost = (select MAX(Cost) from Plans)'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print("User's data for the highest Plan")
    print(result)

    command = 'select User_ID, Name, Joining_Date from User where Plan_ID is null'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print("User's data for no current Plan")
    print(result)

# EMPLOYEE
def no_msg_user():
    command = 'select User_ID, Name, Gender, Joining_Date, Plan_ID from User where User_ID not in (select Sender as "User_ID" from Chats where DATE(Sent_Time) >= DATE(NOW() - INTERVAL 3 MONTH));'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# USER
def show_user_issues():
    command = 'select Issue_ID, Created_time, Resolved from Issues where User_ID={}'
    try:
        cur_obj.execute(command.format(user_id))
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# EMPLOYEE
def users_with_issues():
    command = 'select a.User_ID, Name, Joining_Date, Plan_ID from User a join Issues b on a.User_ID=b.User_ID where Resolved=false group by a.User_ID'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# EMPLOYEE
def users_per_plans():
    command = 'select a.*,count(*) as "No of Users" from Plans a join User b on a.Plan_ID=b.Plan_ID group by (a.Plan_ID)'
    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)

# EMPLOYEE
def users_after_months():
    months = input("Enter no of months: ")

    command = 'select count(*) as "Number of Users" from User where Joining_Date >= DATE(NOW() - INTERVAL {} MONTH)'
    try:
        cur_obj.execute(command.format(months))
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)


# USER
def meta_reality():
    print("Current available Meta-Reality Options are: ")
    command = "select * from MetaReality"
    result = ''

    try:
        cur_obj.execute(command)
        result = from_db_cursor(cur_obj)
    except Exception as e:
        print(e)

    print(result)
    print("\n You can now move onto your Meta-Reality Glasses/Device and start enjoying the feeling of joy....")
    input("Press any key to continue back")

# USER
def show_chats():
    user_id = 2
    command = 'select Name, Content, Sent_time from Chats a join User b on Sender=User_ID where Receiver={}'
    try:
        cur_obj.execute(command.format(user_id))
        result = cur_obj.fetchall()
    except Exception as e:
        print(e)

    for i in result:
        print("\n", i[0], " ~ ", i[2], sep="")
        print(">>", i[1])


"""
FUNCTIONS OVER
MENU STARTS
"""
emp_id = 0
user_id = 0


def admin():
    global user_id
    global emp_id
    user_id = input("User ID: ")
    password = input("PASS: ")

    if (user_id.lower() == "bb" and password.lower() == "boss"):
        while 1:
            print("1. For Raw SQL Execution\n2. For Main Menu")
            i = int(input("> "))
            clear()
            if i == 1:
                raw_sql()
            elif i == 2:
                menu1()
    else:
        print("Wrong Username/Password")
        menu1()


def user():
    global user_id
    global emp_id
    if not user_id:
        user_id = int(input("Enter Your User ID: "))
        # Check id

    while 1:
        print("1. Send chat")
        print("2. Delete User")
        print("3. New Issue")
        print("4. Show Plan")
        print("5. Change Plan")
        print("6. Show Issues")
        print("7. Show Chats")
        print("8. Start Meta-Reality Platform")
        print("9. Go back")

        try:
            i = int(input("> "))
        except Exception as e:
            i = 0
            clear()

        clear()

        if i == 1:
            send_chat()
        elif i == 2:
            delete_user()
        elif i == 3:
            new_issue()
        elif i == 4:
            show_plan()
        elif i == 5:
            show_plan()
            change_plan()
        elif i == 6:
            show_user_issues()
        elif i == 7:
            show_chats()
        elif i == 8:
            meta_reality()
        elif i == 9:
            menu1()
        else:
            print("WRONG INPUT")


def emp():
    global user_id
    global emp_id
    emp_id = int(input("Enter Your Employee ID: "))
    # check id

    while 1:
        print("1. To leave company")
        print("2. Resolve Issue")
        print("3. Show Users with Issues")
        print("4. Show Plans")
        print("5. Update Plan")
        print("6. Show Premium Users")
        print("7. Users with highest and no plans")
        print("8. Users per each plan")
        print("9. Oldest and Newest Active Users")
        print("10. No of Users joined within last n months")
        print("11. Users with no msgs since last 3 months")
        print("12. Go Back to Main Menu")

        try:
            i = int(input("> "))
        except Exception as e:
            i = 0
            clear()

        clear()

        if i == 1:
            leave_company()
            menu1()
        elif i == 2:
            resolve_issue()
        elif i == 3:
            users_with_issues()
        elif i == 4:
            show_plan()
        elif i == 5:
            update_plan()
        elif i == 6:
            premium_users()
        elif i == 7:
            user_high_low_plan()
        elif i == 8:
            users_per_plans()
        elif i == 9:
            old_new_user()
        elif i == 10:
            users_after_months()
        elif i == 11:
            no_msg_user()
        elif i == 12:
            menu1()
        else:
            print("WRONG INPUT")


def menu1():
    global user_id
    global emp_id
    user_id = 0
    emp_id = 0
    print("1. Login as Admin")
    print("2. User Commands")
    print("3. Employee Commands")
    print("4. New User")
    print("9. To Exit")

    try:
        i = int(input("> "))
    except Exception as e:
        i = 0
        clear()

    clear()

    if i == 1:
        admin()
    elif i == 2:
        user()
    elif i == 3:
        emp()
    elif i == 4:
        user_id = new_user()
        user()
    elif i == 9:
        exit(0)
    else:
        print("WRONG INPUT")


try:
    pymysql_obj = pymysql.connect(host="localhost", port=3306, user="hp", password=str(
        os.environ["MYSQL_PASS"]), database="dna_project_team1", autocommit=True)
    cur_obj = pymysql_obj.cursor()
except Exception as e:
    print(e)
    exit(0)

menu1()

cur_obj.close()
pymysql_obj.close()
