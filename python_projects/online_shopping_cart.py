class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def display_product(self):
        print(f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock}")

    def update_stock(self, quantity):
        self.stock += quantity

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product.stock >= quantity:
            if product.product_id in self.items:
                self.items[product.product_id]['quantity'] += quantity
            else:
                self.items[product.product_id] = {'product': product, 'quantity': quantity}
            product.update_stock(-quantity)
            print(f"Added {quantity} of {product.name} to cart.")
        else:
            print(f"Not enough stock for {product.name}. Available: {product.stock}")

    def remove_item(self, product_id, quantity):
        if product_id in self.items:
            current_quantity = self.items[product_id]['quantity']
            product = self.items[product_id]['product']
            if quantity >= current_quantity:
                product.update_stock(current_quantity)
                del self.items[product_id]
                print(f"Removed all {product.name} from cart.")
            else:
                self.items[product_id]['quantity'] -= quantity
                product.update_stock(quantity)
                print(f"Removed {quantity} of {product.name} from cart.")
        else:
            print(f"Product with ID {product_id} not found in cart.")

    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print("\n--- Your Shopping Cart ---")
        total_price = 0
        for item_id, item_data in self.items.items():
            product = item_data['product']
            quantity = item_data['quantity']
            item_total = product.price * quantity
            total_price += item_total
            print(f"{product.name} (x{quantity}) - ${product.price:.2f} each, Total: ${item_total:.2f}")
        print(f"--------------------------")
        print(f"Total Cart Value: ${total_price:.2f}")

    def checkout(self):
        if not self.items:
            print("Cannot checkout, cart is empty.")
            return 0
        total_cost = sum(item['product'].price * item['quantity'] for item in self.items.values())
        print(f"\nCheckout successful! Your total is: ${total_cost:.2f}")
        self.items = {}
        return total_cost

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.shopping_cart = ShoppingCart()

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"

# Example Usage:
if __name__ == "__main__":
    # Create some products
    product1 = Product("P001", "Laptop", 1200.00, 10)
    product2 = Product("P002", "Mouse", 25.00, 50)
    product3 = Product("P003", "Keyboard", 75.00, 20)

    # Create a customer
    customer1 = Customer("C001", "Alice", "alice@example.com")
    print(customer1)

    # Add items to cart
    customer1.shopping_cart.add_item(product1, 1)
    customer1.shopping_cart.add_item(product2, 2)
    customer1.shopping_cart.add_item(product3, 1)
    customer1.shopping_cart.add_item(product1, 5) # Add more laptops
    customer1.shopping_cart.add_item(product2, 60) # Not enough stock

    # View cart
    customer1.shopping_cart.view_cart()

    # Remove an item
    customer1.shopping_cart.remove_item("P002", 1)
    customer1.shopping_cart.view_cart()

    # Checkout
    customer1.shopping_cart.checkout()
    customer1.shopping_cart.view_cart()

    print("\n--- Product Stock After Operations ---")
    product1.display_product()
    product2.display_product()
    product3.display_product()