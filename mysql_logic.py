from datetime import date
import mysql.connector
import logging
from Order import Order
from Account import Account    
from Product import Product   

logging.basicConfig(filename="sql.logs", level=logging.DEBUG, format='%(asctime)s :: %(message)s')

cnx = mysql.connector.connect(user="root", password="200188348Jt!",
                              host="127.0.0.1", database = "naviecommerce")
cursor = cnx.cursor()

cursor.execute("SELECT * FROM user")
print(cursor.fetchall())

def insert_user(user: Account):
    new_user = f"INSERT INTO user(email, role, name) VALUES('{user.get_email()}', '{user.get_role()}', '{user.get_name()}');"
    cursor.execute(new_user)
    cnx.commit()
    logging.info(f"adding new user - id: {cursor._last_insert_id} name: {user.get_name().title()}")
    insert_credentials(user)  
  
def insert_credentials(user: Account):
    id_sql= f"SELECT id FROM user WHERE email = '{user.get_email()}'; "
    cursor.execute(id_sql)
    id = cursor.fetchone()[0]
    user.set_id(id)

    new_credentials = f"INSERT INTO credentials(userID, username, password) VALUES({user.get_id()}, '{user.get_username()}', '{user.get_password()}');"
    cursor.execute(new_credentials)
    cnx.commit()

def get_products():
    sql = "SELECT * FROM products"
    cursor.execute(sql)
    products = []
    for x in cursor.fetchall():
        product = Product(x[0],x[1],x[2],x[3],x[4])
        products.append(product)
    return products
        
def find_user_by_email(email):
    sql_user = f"SELECT * FROM user WHERE email = '{email}' "
    cursor.execute(sql_user)
    return cursor.fetchone()

def find_user_by_username(username):
    sql_user = f"SELECT * FROM user JOIN credentials ON user.id = credentials.userID WHERE userName = '{username}' "
    cursor.execute(sql_user)
    return cursor.fetchone()

def find_user_by_id(id):
    sql_user = f"SELECT * FROM user WHERE user.id = {id} "
    cursor.execute(sql_user)
    return cursor.fetchone()

def check_credentials(username, password):
    sql_account = f"SELECT * FROM user JOIN credentials c ON user.id = c.userID WHERE username = '{username}' AND password = '{str(password)}'"
    cursor.execute(sql_account)
    results = cursor.fetchone()
    try:
        account = Account(username, password,results[1],results[2],results[3], results[0])
    except TypeError:
        account = None
    return account


def insert_into_orders(order: Order):
    sql = "INSERT INTO orders(user_id, ordered_date) VALUES(%s,%s)"
    cursor.execute(sql, (order.user_id, date.today()) )
    order.id = cursor.lastrowid
    insert_into_order_lines(order)
    cnx.commit()
    logging.debug(f"Inserting a new order - id: {order.id}")

def insert_into_order_lines(order:Order):
    
    sql = """INSERT INTO order_lines(order_id, product_id, price, quantity)
            VALUES(%s, %s, %s, %s)"""
    qry = []
    for x in set(order.products):
        id = x.id
        qry.append((order.id, id, order.get_prices()[id], order.prod_qty()[id] ))
    cursor.executemany(sql, qry)

def get_previous_user_orders(account: Account):
    sql = """SELECT o.id, o.user_id, o.ordered_date, p.title, p.image, p.description,
    p.price, ol.quantity, p.id FROM orders o JOIN order_lines ol ON o.id = ol.order_id
    JOIN products p ON ol.product_id = p.id
    WHERE ol.order_id = %s"""

    sql_orders = "SELECT * FROM orders WHERE user_id = %s"
    cursor.execute(sql_orders, [account.get_id()])
    orders_qry = cursor.fetchall()
    order_history = []
    for o in orders_qry:
        products = []
        cursor.execute(sql, [o[0]] )
        for x in cursor:
            for e in range(x[7]):
                products.append(Product(x[8],x[3],x[4],x[5],x[6]))
        order_history.append(Order(o[0], o[1], o[2], products))
    account.set_order_history(order_history)
    account.get_order_history()
    
def get_all_users():
    sql ="SELECT c.username, c.password, u.email, u.role, u.name, c.userid FROM user u JOIN credentials c ON c.userid = u.ID;"
    cursor.execute(sql)
    users = []
    for x in cursor:
        users.append(Account(x[0], x[1], x[2], x[3], x[4], x[5]))
    return users

def modify_user_by_id(id, atr, change):
    sql = f"UPDATE user SET {atr} = %s WHERE id = %s"
    cursor.execute(sql, (change, id))
    cnx.commit()
    logging.debug(f"modifying the user - id: {id} - {atr} to {change}")
    
def modify_credential_by_id(id, atr, change):
    sql = f"UPDATE credentials SET {atr} = %s WHERE userid = %s"
    cursor.execute(sql, (change, id))
    cnx.commit()
    logging.debug(f"modifying the user - id: {id} - {atr} to {change}")

def del_user_and_credentials_by_id(id):
    sql = """DELETE c, u FROM credentials c 
            JOIN user u on c.userid = u.id 
            WHERE c.userID = %s;"""
    sql_ord = """DELETE o, ol FROM orders o 
                JOIN order_lines ol ON o.id = ol.order_id
                WHERE o.user_id = %s"""
    cursor.execute(sql_ord,[id])
    cursor.execute(sql,[id])
    cnx.commit()
    logging.debug(f"deleted user_id: {id} and all their orders")

def delete_past_order_by_id(id):
    sql = "DELETE o, ol FROM orders o LEFT JOIN order_lines ol ON o.id = ol.order_id WHERE o.id = %s;"
    cursor.execute(sql, [id])
    cnx.commit()
    logging.debug(f"Deleted Order #{id}")

def add_to_products(product: Product):
    sql = "INSERT INTO products(title,image,description,price) VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (product.title, product.image, product.description, product.price))
    cnx.commit()
    logging.debug(f"Adding {product.title} to products")

def delete_product_by_id(id):
    sql = "DELETE p FROM products p WHERE p.id = %s"
    cursor.execute(sql, [id])
    cnx.commit()
    logging.debug(f"product #{id} has been deleted")
    # print(products)
# # print(finduser_by_username(test_account))

# delete_product_by_id(21)

# insert_user(test_account)
# print(test_account.get_id())

# products = [Product(1, "one", None, None, 20.99),Product(1, "one", None, None, 20.99),Product(1, "one", None, None, 20.99), Product(2, "two", None, None, 25.99),  Product(2, "two", None, None, 25.99),  Product(2, "two", None, None, 25.99),  Product(3, "three", None, None, 30.99), Product(3, "three", None, None, 30.99),Product(3, "three", None, None, 30.99),Product(3, "three", None, None, 30.99),Product(3, "three", None, None, 30.99)]
# account = Account(None, None, 'e', 'e', 'e', 5)
# get_previous_user_orders(account)
# account.set_cart(products)
# account.remove_from_cart(5, 5)
# order = Order(0, 1, 10-14,products)
# insert_into_orders(order)
# print(order.prod_qty())
# order.get_prices()

# print(order.products)
# print(order.get_total_price())







