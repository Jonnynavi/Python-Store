class Product():
    def __init__(self,id,title,image,description,price):
        self.id = id
        self.title = title
        self.image = image
        self.description = description
        self.price = price

    def __repr__(self):  
        return f"id: {self.id}, \ntitle: {self.title} \nimage: {self.image} \ndescription: {self.description} \nprice: ${self.price}"

    def __eq__(self, product):
        return self.title == product.title
    def __hash__(self):
      return hash((self.id, self.title, self.price))
    
