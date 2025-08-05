# ecommerce.py

import uuid


class User:
    def _init_(self, username, email):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.cart = Cart(self)

    def _str_(self):
        return f"{self.username} ({self.email})"


class Product:
    def _init_(self, name, price, stock):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.stock = stock

    def _str_(self):
        return f"{self.name} - ${self.price} ({self.stock} in stock)"


class Cart:
    def _init_(self, user):
        self.user = user
        self.items = {}

    def add_product(self, product, quantity):
        if product.stock < quantity:
            print(f"Only {product.stock} units available.")
            return
        if product.product_id in self.items:
            self.items[product.product_id]['quantity'] += quantity
        else:
            self.items[product.product_id] = {'product': product, 'quantity': quantity}
        print(f"Added {quantity} x {product.name} to cart.")

    def remove_product(self, product):
        if product.product_id in self.items:
            del self.items[product.product_id]
            print(f"Removed {product.name} from cart.")

    def view_cart(self):
        if not self.items:
            print("Cart is empty.")
            return
        print("🛒 Cart items:")
        total = 0
        for item in self.items.values():
            p = item['product']
            q = item['quantity']
            print(f"  {p.name} - ${p.price} x {q} = ${p.price * q}")
            total += p.price * q
        print(f"Total: ${total:.2f}")

    def checkout(self):
        if not self.items:
            print("Cart is empty.")
            return
        order = Order(self.user, self.items)
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            product.stock -= quantity
        self.items = {}  # Clear cart after checkout
        print("✅ Order placed successfully!")
        order.show_summary()


class Order:
    def _init_(self, user, items):
        self.order_id = str(uuid.uuid4())
        self.user = user
        self.items = items

    def show_summary(self):
        print(f"🧾 Order ID: {self.order_id}")
        total = 0
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            cost = product.price * quantity
            print(f"{product.name} - {quantity} x ${product.price} = ${cost}")
            total += cost
        print(f"Total Amount: ${total:.2f}")


# Demo data setup
def main():
    # Products
    p1 = Product("Laptop", 1200.00, 10)
    p2 = Product("Headphones", 150.00, 20)
    p3 = Product("Keyboard", 80.00, 15)

    # User
    user1 = User("john_doe", "john@example.com")

    print(f"Welcome, {user1.username}!")
    print("\nAvailable Products:")
    for p in [p1, p2, p3]:
        print(f"  - {p}")

    # Simulate cart operations
    user1.cart.add_product(p1, 1)
    user1.cart.add_product(p2, 2)
    user1.cart.view_cart()

    # Remove one item
    user1.cart.remove_product(p2)
    user1.cart.view_cart()

    # Checkout
    user1.cart.checkout()

    # View remaining stock
    print("\n📦 Remaining Stock:")
    for p in [p1, p2, p3]:
        print(f"  - {p}")


if _name_ == "_main_":
    main()
