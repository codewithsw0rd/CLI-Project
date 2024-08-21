# CLI project:- command line interface is a text-base interface where you can input commands that interact with the computers operating system.
#CRUD = CREATE, READ, UPDATE and DELETE.

import sqlite3 
import csv 

# now we push this file in github
# git is a version control system.
# git hub helps us to keep track of the program
# SOME GIT COMMANDS:- 
# git init
# git add .
# git commit -m"Your commit message"
# git push origin main
# git diff


# Function to create a connection to the sqlite database.
def create_connection():
    try:
        conn = sqlite3.connect("users.sqlite3")
        return conn
    except Exception as e:
        print("Error: {e}")

# Menu options string for user interaction
INPUT_STRING = """
******************************************************************
Enter the option:
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from TABLE
    5. QUERY user by ID from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE user by ID
    9. UPDATE user
    10. Press any key to EXIT
***********************************************************************
"""

# Function to create a "users" table if it doesnt exist.
def create_table(conn):
    CREATE_USERS_TABLE_QUERY ="""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        );
    """
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table was created succesfully.")    


# Function to read users from a csv file
def read_csv():
    users = []
    with open("sample_users.csv", "r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]

# Function to insert the list of users into the 'users' table.
def insert_users(con, users):
    user_add_query = """
        INSERT INTO users
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web    
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()
    print(f"{len(users)} users were imported successfully.")

# Function to querry all users or specified number of users.
def select_users(con, no_of_users = 0):
    cur = con.cursor()
    if no_of_users :
        users = cur.execute("SELECT * FROM users LIMIT ?", (no_of_users,))
    else :
        users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

# Function to querry and print a user by id.
def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
    for user in users:
        print(user)

# Function to delete all users from a users table
def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("All users were deleted successfully.")

# Function to delete a specified user by id
def delete_user_by_id(con, user_id):
    cur= con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    con.commit()
    print(f"User with id {user_id} was successfully deleted.")

# List of columns name in the users table
columns = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)   

# Function to update a specific column of a user by id
def update_user_by_id(con,user_id, column_name, column_value):
    update_query = f"UPDATE users set {column_name} = ? where id = ?;"
    cur = con.cursor()
    cur.execute(update_query, (column_value, user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with value[{column_value}] of user with id[{user_id}]"
    )

# Main function to handle user input and perforn CRUD operations.
def main():
    con = create_connection()

    while True:
        user_input = input(INPUT_STRING)

        if user_input == "1":
            create_table(con)

        elif user_input == "2":
            delete_users(con)
            users = read_csv()
            insert_users(con, users)
            
        elif user_input == "3":
            data = []
            for column in columns:
                column_value = input(f"Enter the value of {column}: ")
                data.append(column_value)
            insert_users(con, [tuple(data)])

        elif user_input == "4":
            select_users(con)

        elif user_input == "5":
            user_id = input('Enter user id: ')
            if user_id.isnumeric():
                select_user_by_id(con, user_id)

        elif user_input == "6":
            no_of_users = input("Enter no of users to fetch:- ")
            if no_of_users.isnumeric() and int(no_of_users)>0 :
                select_users(con, no_of_users = int(no_of_users))

        elif user_input == "7":
            confirm  = input("Are you sure you want to delete all the users? (y/n) :- ")
            if confirm == "y":
                delete_users(con)

        elif user_input == "8":
            user_id =input("Enter user id:- ")

            if user_id.isnumeric() :
                delete_user_by_id(con, user_id)
                
        elif user_input == "9":
            user_id = input("Enter id of user: ")
            if user_id.isnumeric() :
                column_name = input(
                    f"""Enter the column you want to edit.\nPlease make sure column is within:\n [{columns}]\n"""
                )
                if column_name in columns:
                    column_value = input(f"Enter the value of {column_name}: ")
                    update_user_by_id(con, user_id, column_name, column_value)
        else:
            break


if __name__ ==  "__main__":
    main() # executes the main function when the script is run

