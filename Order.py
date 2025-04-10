class Order():
    def __init__(self, id, user_id, order_date, products=[]):
        self.id = id
        self.user_id = user_id
        self.order_date = order_date
        self.products = products
        self.total_price = sum([x.price for x in products])

    def add_product(self, product):
        self.products.append(product)
    
    def prod_qty(self):
        id_qty = {x.id:self.products.count(x) for x in self.products}
        return id_qty
    
    def get_prices(self):
        id_price = { x.id : x.price * self.products.count(x) for x in self.products}
        return id_price
    
    def __repr__(self):  
        return f"\n-------------------------------------\nid: {self.id}, \ndate: {self.order_date} \nproducts: {self.products}"
    
    def get_total_price(self):
        return sum([ x.price for x in self.products])
