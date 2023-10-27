# 'pip install pymysql' to be able to establish a connection to a MySQL database

import pymysql

class db:
    def __init__(x):
        x.connection = None
        x.cursor = None

#  The connection to the database is established

    def connect(x):
        x.connection = pymysql.connect(
            host ='localhost',
            user ='root',
            password = '',
            db = 'testdatabase'
        )
        
        x.cursor = x.connection.cursor()

        print("<==== Succesfully connected to Database ====>")

# Close connection

    def close_connection(x):
        if x.connection:
            x.connection.close()

# method for inserting people into the 'people' table

    def insert_people(x, id_user, name, last_name):
        try:
            x.cursor.execute("SELECT id_user FROM people WHERE id_user = $s", (id_user,))
            person_exist = x.cursor.fetchone()

            if person_exist:
                print(f"The person identified with {id_user} there exist, please, try with another ID")
            else:
                x.cursor.execute("INSERT INTO people (id_user, name, last_name) VALUES (%s, %s, %s)",
                (id_user, name, last_name))
                
                x.connection.commit()
                print(f"{name} has been inserted")

        except pymysql.Error as xd:
            print(f"There was an error while trying to insert: {xd}")

    def insert_product(x, id_product, client_name, products_amount):
        try:
            x.cursor.execute(
                "INSERT INTO products (id_product, client_name, products_amount) VALUES (%s, %s, %s)",
                (id_product, client_name, products_amount)
            )
            x.connection.commit()
            print("Product/s added")
        except pymysql.Error as xd:
            print(f"There was an error while trying to insert: {xd}")

# Instance for DB class

database = db()

class users:

    def __init__(x, user, password):
        x.__user = user
        x.__password = password

    def got_user(x):
        return x.__user
    
    def set_pass(x, password):
        x.__password = password

    def log(x, got_pass):
        return x.__password == got_pass
    
    def __str__(x):
        return f'User: {x.__user}'
    
class admin(users):
    def __init__(x, user, password):
        super().__init__(user, password)

    def __str__(x):
        return f'Admin User: {x.got_user}'
    
class people(users):
    def __init__(x, user, password):
        super().__init__(user, password)

    def __str__(x):
        return f'Regular user: {x.got_user}'
    
def print_user_info(username):
    print(username)

if_admin = lambda username: isinstance(username, admin)

administrator = admin("admin", "1234")
classic_user = people("user", "1234")

def loginmenu():
    while True:
        print("1. Login")
        print("2. Exit")
        option = input("Select an option: ")

        if option == "1":
            user = input("User: ")
            password = input("Pass: ")

            if administrator.got_user() == user and administrator.log(password):
                database = connect()
                print("<=== ----- ===>")
                print("Login Succesfully")
                print("<=== ----- ===>")
                print_user_info(administrator)
                while True:
                    admin_option = input("Would you like to add a person? (y/n): ").lower()
                    if admin_option == "y":
                        id_user = input("ID: ")
                        name = input("Name: ")
                        last_name = input("Last name: ")

                        database.insert_people(id_user, name, last_name)
                        print(f"{name} added succesfully")
                    elif admin_option == "n":
                        break
                    else:
                        print("Enter a valid option")
            elif classic_user.got_user() == user and classic_user.log(password):
                database.connect()
                print("<=== ----- ===>")
                print("Login Succesfully")
                print("<=== ----- ===>")
                print_user_info(classic_user)
                while True:
                    classic_option = input("Would you like to add a product? (y/n): ").lower()
                    if classic_option == "y":
                        id_product = input("ID: ")
                        client_name = input("Client name: ")
                        products_amount = input("Products amount: ")

                        database.insert_product(id_product, client_name, products_amount)
                        print(f"Product/s inserted succesfully")
                    elif classic_option == "n":
                        break
                database.close()
            else:
                print("User or pass incorrect, please try again")
        elif option == "2":
            database.close()
            break
        else:
            print("Invalid option")

loginmenu()