create table
    IF NOT EXISTS Employees (
        Employee_ID int Primary Key AUTO_INCREMENT,
        Employee_Name varchar(45) not NULL,
        Department varchar(20),
        Supervisor_ID int,
        Foreign Key (Supervisor_ID) references Employees(Employee_ID) ON UPDATE
        SET NULL
    );

create table
    IF NOT EXISTS Plans (
        Plan_ID int Primary Key AUTO_INCREMENT,
        Cost decimal(8, 2) check(Cost > 0),
        Duration int check(Duration > 0) -- In Days
    );

create table
    IF NOT EXISTS Plans_Features (
        Plan_ID int not null,
        Features varchar(100) not null,
        Primary Key(Plan_ID, Features),
        Foreign Key (Plan_ID) references Plans(Plan_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS User (
        User_ID int Primary Key AUTO_INCREMENT,
        Aadhar_Number bigint not NULL UNIQUE,
        Name varchar(45) not NULL,
        Gender varchar(10) check(
            Gender in (
                'Male',
                'Female',
                'Others',
                'M',
                "F",
                'O'
            )
        ),
        DOB date not NULL,
        Joining_Date date DEFAULT (CURRENT_DATE),
        Plan_ID int,
        -- can be null if user doesn't have any plan
        Foreign Key (Plan_ID) references Plans(Plan_ID) ON UPDATE CASCADE ON DELETE
        SET NULL
    );

create table
    IF NOT EXISTS Photos (
        User_ID int not null,
        Entry_Location varchar(50) not null,
        Media_Size bigint check(Media_Size > 0),
        Media_Data LONGBLOB ,
        Primary Key(User_ID, Entry_Location),
        Foreign Key (User_ID) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Chats (
        Sender int not null,
        Receiver int not null,
        Sent_Time TIMESTAMP default CURRENT_TIMESTAMP not null,
        Content varchar(500),
        Primary Key(Sender, Receiver, Sent_time),
        Foreign Key (Sender) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE,
        Foreign Key (Receiver) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Issues (
        Issue_ID int Primary Key AUTO_INCREMENT,
        Created_time DATETIME default CURRENT_TIMESTAMP not null,
        User_ID int,
        Employee_ID int,
        -- can be null, until solved
        Resolved BOOLEAN DEFAULT false,
        Content varchar(500),
        Foreign Key (User_ID) references User(User_ID) ON UPDATE CASCADE ON DELETE
        SET
            NULL,
            Foreign Key (Employee_ID) references Employees(Employee_ID) ON UPDATE CASCADE ON DELETE
        SET NULL
    );

create table
    IF NOT EXISTS MetaReality (
        Location varchar(50) Primary Key,
        Time datetime not null,
        Climate varchar(40) not null
    );

create table
    IF NOT EXISTS Preferences (
        User_ID int not null,
        Age int,
        Description varchar(100),
        Gender varchar(10) check(
            Gender in ('Male', 'Female', 'Others')
        ),
        Foreign Key (User_ID) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Preferance_Language (
        User_ID int not null,
        Language varchar(50) not null,
        Primary Key(User_ID, Language),
        Foreign Key (User_ID) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Preferance_Country (
        User_ID int not null,
        Country varchar(50) not null,
        Primary Key(User_ID, Country),
        Foreign Key (User_ID) references User(User_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Makes (
        Plan_ID int not null,
        Employee_ID int not null,
        Cost_to_Comapany int check(Cost_to_Comapany > 0),
        Primary Key(Plan_ID, Employee_ID),
        Foreign Key (Plan_ID) references Plans(Plan_ID) ON UPDATE CASCADE ON DELETE CASCADE,
        Foreign Key (Employee_ID) references Employees(Employee_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table
    IF NOT EXISTS Maintains (
        MetaReality_Loc varchar(50) not null,
        Employee_ID int not null,
        Duration int check(Duration > 0),
        -- in hours
        Primary Key(MetaReality_Loc, Employee_ID),
        Foreign Key(MetaReality_Loc) references MetaReality(Location) ON UPDATE CASCADE ON DELETE CASCADE,
        Foreign Key (Employee_ID) references Employees(Employee_ID) ON UPDATE CASCADE ON DELETE CASCADE
    );

-- ADD ON UPDATE CASCADE COMMANDS FOR ALL FOREIGN KEYS