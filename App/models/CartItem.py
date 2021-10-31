class CartItem():
    product_slug = ""
    current_price = 0

    def __init__(self, product_slug, current_price):
        self.product_slug = product_slug
        self.current_price = current_price