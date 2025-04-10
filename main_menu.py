from Account import Account
from Product import Product
from mysql_logic import *

def login():
    print("please enter your info")
    username = input("Username: ")
    password = input("Password: ")
    account = check_credentials(username, password)
    if account == None:
        print("please try again your username or password was incorrect")
    else:
        return account
    
def create_an_account():
    email = input("Please enter your email\n")
    while True:
        does_email_exist = find_user_by_email(email)
        if does_email_exist != None:
            print("Email is already in use please try another one")
            email = input("Please enter your email\n")
            continue
        else:
            break
    username = input("Please create a username\n")
    while True:
        does_username_exist = find_user_by_username(username)
        if does_username_exist != None:
            print("Username is already in use please try again")
            username = input("Please create a username\n")
            continue
        else:
            break
        
    password = input("Please create a password\n")
    first_name = input("Please enter your first name\n")
    last_name = input("please enter your last name\n")
    full_name = first_name + " " + last_name
    secret_code = input("if your are an employee please enter the secret code\n")
    if secret_code == "1234":
        role = "admin"
    else:
        role = "customer"
        
    account = Account(username, password, email, role, full_name)
    insert_user(account)
    print(f"Thank you for creating an account {first_name}")
    return account

def show_products():
    print("Current Items")
    products = get_products()
    print("id | title | description | price")
    for x in products:
        print(f"{x.id} | {x.title} | {x.description} | ${x.price}")
        print("--------------------------------------------------------------------------------------------")
    return products


def add_to_cart(product:Product, current_user: Account):
    current_user.add_to_cart(product)

# def remove_item_from_cart(current_user: Account):
#     A
 
def check_out(user: Account):
    order = Order(None, user.get_id(),date.today(),user.get_cart())
    insert_into_orders(order)
    print(f"Order #{order.id} has been Placed")
    user.empty_cart()

def get_user_prev_orders(account: Account):
    get_previous_user_orders(account)
    account.get_order_history()

def list_users():
        users = get_all_users()
        print("##################")
        print("       users      ")
        print("##################")
        for x in users:
            print(f"userID: {x.get_id()} | {x.get_username()} | {x.get_email()} | {x.get_name()}")
            print("---------------")

def users_orders():
    while True:
        list_users()
        id = input("Please enter the ID of the order history you would like to view or enter 0 to quit\n")
        if id == "0":
            return
        elif find_user_by_id(int(id)) == None:
            print("That id currently does not exist, try again.")
            continue
        while True:
            account = Account(None, None,None,None,None, int(id))
            get_previous_user_orders(account)
            order_id = input("Please enter the ID for the order you wish to delete or enter 0 to quit\n")
            if order_id == "0":
                return
            delete_past_order_by_id(order_id)
            
        
def edit_users():
    while True:
        list_users()
        id = input("Select a user to edit from the provided IDs, or enter 0 to quit\n")
        if id == "0":
            return
        elif find_user_by_id(id) == None:
            print("That id currently does not exist, try again.")
            continue

        while True:
            print("###################")
            print("     Edit Menu     ")
            print("###################")
            choice = input("Choose what you would like to do \n1.change username\n2.change password\n3.change email\n4.change name\n5.delete user \n6.abort\n")
            match choice:
                case "1":
                    try:
                        modify_credential_by_id(id, "username", input("new username: "))
                    except:
                        print("!!!Username is already taken, please choose a different one!!!")
                case "2":
                    modify_credential_by_id(id, "password", input("new password: "))
                case "3":
                    try:
                        modify_user_by_id(id, "email", input("email: "))
                    except:
                        print("!!!Email is already taken, please choose a different one!!!")

                case "4":
                    modify_user_by_id(id, "name", input("first name: ") + " " + input("last name: "))
                case "5":
                    if input("are you sure? y/n\n") == "y":
                        del_user_and_credentials_by_id(id)
                        break
                    else:
                        continue
                case "6":
                    break

def edit_products():
        while True:
            print("###################")
            print("    Prodcut Menu   ")
            print("###################")
            choice = input("1.add product\n2.delete product\n3.list products\n4.quit\n")
            match choice:
                case "1":
                    add_product()
                case "2":
                    delete_product()
                case "3":
                    show_products()
                case "4":
                    break          

def add_product():
    title = input("Enter a name of item\n")
    image = input("Enter Image\n")
    description = input("Enter item description\n")
    while True:
        try:
            price = int(input("Enter item price\n"))
        except:
            print("incorrect input, try again")
            continue
        break
    add_to_products(Product(None, title, image, description, price))

def delete_product():
    show_products()
    while True:
        try:
            id = input("Enter Product ID\n")
        except:
            print("Incorrect input, try again")
            continue
        break
    delete_product_by_id(id)
    print("_______________________________")
    print(f"Product {id} has been deleted")
    print("_______________________________")