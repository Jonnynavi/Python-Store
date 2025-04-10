
class Account():
    def __init__(self, username, password, email, role, name, id=None):
        self._id = id
        self._username = username
        self._password = password
        self._email = email
        self._role = role
        self._name = name
        self._cart = []
        self._order_history = []
    

    def get_id(self):
        return self._id

    def get_email(self):
        return self._email
    
    def get_role(self):
        return self._role

    def get_name(self):
        return self._name.title()
    
    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password
    
    def add_to_cart(self, product, qty):
        for x in range(qty):
            self._cart.append(product)  
    

    def reduce_qty_cart(self, id, qty):
        selected = [x for x in self._cart if x.id == id]
        if qty > len(selected):
            qty = len(selected)
        for x in selected:
            self._cart.remove(x)
            qty -= 1
            if qty < 1:
                break

    def increase_qty_cart(self, id, qty):
        selected = [x for x in self._cart if x.id == id]
        for x in range(qty):
            try:
                self._cart.append(selected[0])
            except IndexError:
                print("Please choose from the avaliable ids")
                return
    def empty_cart(self):
        self._cart = []

    def set_id(self, id):
        self._id = id
    
    def get_cart(self):
        return self._cart
    
    def set_cart(self, cart):
        self._cart = cart

    def get_price_line(self):
        res = []
        [res.append(x) for x in self._cart if x not in res]
        print("--------------------------------")
        total_price = sum([x.price for x in self._cart])
        for x in res:
            print(f"id: {x.id} | {x.title} | qty: {self._cart.count(x)} | price: {'${0}'.format(format(x.price * self._cart.count(x), ',.2f'))}")
        print(f"your total price is {'${0}'.format(format(total_price, ',.2f'))}")
        print("--------------------------------")
    
    def __repr__(self):  
        return f"id: {self._id}, \nemail: {self._email} \nrole: {self._role} \nname: {self._name}" 
    
    def get_order_history(self):
        for i in self._order_history:
            print("____________________________________________________")
            print("###########################")
            print(f"Order #{i.id}")
            print("###########################")
            res = []
            [res.append(x) for x in i.products if x not in res]
            print("--------------------------------")
            total_price = i.get_total_price()
            for x in res:
                print(f"id: {x.id} | {x.title} | qty: {i.products.count(x)} | price: {'${0}'.format(format(x.price * i.products.count(x), ',.2f'))}")
            print(f"your total price is {'${0}'.format(format(total_price, ',.2f'))}")
            print("--------------------------------")
        return self._order_history
    
    def find_order(self, id):
        for i in self._order_history:
            if i.id == int(id):
                return i
        return None
    def set_order_history(self, history):
        self._order_history = history