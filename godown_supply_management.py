import datetime

class Product:
    def __init__(self, product_id, name, category, unit_price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.unit_price = unit_price

    def __str__(self):
        return f"Product ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: ${self.unit_price:.2f}/unit"

class InventoryItem:
    def __init__(self, product, quantity, last_updated=None):
        self.product = product
        self.quantity = quantity
        self.last_updated = last_updated if last_updated else datetime.datetime.now()

    def update_quantity(self, change):
        self.quantity += change
        self.last_updated = datetime.datetime.now()
        if self.quantity < 0:
            self.quantity = 0 # Prevent negative stock
            print(f"Warning: Quantity for {self.product.name} went below zero. Set to 0.")

    def __str__(self):
        return f"Item: {self.product.name}, Quantity: {self.quantity}, Last Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"

class Godown:
    def __init__(self, godown_id, name, location, capacity):
        self.godown_id = godown_id
        self.name = name
        self.location = location
        self.capacity = capacity # Max items or volume
        self.inventory = {}

    def add_product_to_inventory(self, product, quantity):
        if product.product_id in self.inventory:
            self.inventory[product.product_id].update_quantity(quantity)
            print(f"Updated quantity for {product.name} in {self.name}. New quantity: {self.inventory[product.product_id].quantity}")
        else:
            if self.get_current_stock_count() + quantity <= self.capacity:
                self.inventory[product.product_id] = InventoryItem(product, quantity)
                print(f"Added {quantity} units of {product.name} to {self.name}.")
            else:
                print(f"Cannot add {quantity} units of {product.name} to {self.name}. Capacity exceeded.")

    def remove_product_from_inventory(self, product_id, quantity):
        if product_id in self.inventory:
            item = self.inventory[product_id]
            if item.quantity >= quantity:
                item.update_quantity(-quantity)
                print(f"Removed {quantity} units of {item.product.name} from {self.name}. Remaining: {item.quantity}")
                if item.quantity == 0:
                    del self.inventory[product_id]
                    print(f"Product {item.product.name} removed from inventory as stock is zero.")
                return True
            else:
                print(f"Not enough stock of {item.product.name} in {self.name} to remove {quantity} units. Available: {item.quantity}")
                return False
        else:
            print(f"Product ID {product_id} not found in {self.name} inventory.")
            return False

    def get_product_stock(self, product_id):
        item = self.inventory.get(product_id)
        return item.quantity if item else 0

    def get_current_stock_count(self):
        return sum(item.quantity for item in self.inventory.values())

    def get_inventory_value(self):
        return sum(item.product.unit_price * item.quantity for item in self.inventory.values())

    def __str__(self):
        return (f"Godown ID: {self.godown_id}, Name: {self.name}, Location: {self.location}, "
                f"Capacity: {self.get_current_stock_count()}/{self.capacity}")

class SupplyManagementSystem:
    def __init__(self):
        self.godowns = {}
        self.products = {}

    def add_godown(self, godown):
        if godown.godown_id not in self.godowns:
            self.godowns[godown.godown_id] = godown
            print(f"Godown {godown.name} added to the system.")
        else:
            print(f"Godown {godown.name} already exists.")

    def add_product(self, product):
        if product.product_id not in self.products:
            self.products[product.product_id] = product
            print(f"Product {product.name} added to the system.")
        else:
            print(f"Product {product.name} already exists.")

    def get_godown(self, godown_id):
        return self.godowns.get(godown_id)

    def get_product(self, product_id):
        return self.products.get(product_id)

    def transfer_product(self, product_id, quantity, from_godown_id, to_godown_id):
        from_godown = self.get_godown(from_godown_id)
        to_godown = self.get_godown(to_godown_id)
        product = self.get_product(product_id)

        if not (from_godown and to_godown and product):
            print("Error: One or more of Godown/Product not found for transfer.")
            return False

        if from_godown.remove_product_from_inventory(product_id, quantity):
            to_godown.add_product_to_inventory(product, quantity)
            print(f"Successfully transferred {quantity} units of {product.name} from {from_godown.name} to {to_godown.name}.")
            return True
        else:
            print(f"Transfer failed for {product.name} from {from_godown.name} to {to_godown.name}.")
            return False

    def get_total_inventory_value_system(self):
        return sum(godown.get_inventory_value() for godown in self.godowns.values())

    def __str__(self):
        return (f"Supply Management System | Godowns: {len(self.godowns)} | "
                f"Products: {len(self.products)}")

# Example Usage:
if __name__ == "__main__":
    system = SupplyManagementSystem()
    print(system)

    # Add products
    prod1 = Product("P001", "Laptop", "Electronics", 1200.00)
    prod2 = Product("P002", "Mouse", "Electronics", 25.00)
    prod3 = Product("P003", "Chair", "Furniture", 150.00)
    prod4 = Product("P004", "Table", "Furniture", 200.00)

    system.add_product(prod1)
    system.add_product(prod2)
    system.add_product(prod3)
    system.add_product(prod4)

    # Add godowns
    godown_a = Godown("G001", "Main Warehouse", "New York", 1000)
    godown_b = Godown("G002", "Regional Depot", "Los Angeles", 500)

    system.add_godown(godown_a)
    system.add_godown(godown_b)

    # Add products to godown A
    godown_a.add_product_to_inventory(prod1, 50)
    godown_a.add_product_to_inventory(prod2, 200)
    godown_a.add_product_to_inventory(prod3, 30)

    # Add products to godown B
    godown_b.add_product_to_inventory(prod1, 20)
    godown_b.add_product_to_inventory(prod4, 40)

    print("\n--- Godown A Inventory ---")
    for item in godown_a.inventory.values():
        print(item)
    print(f"Godown A Current Stock: {godown_a.get_current_stock_count()}")
    print(f"Godown A Inventory Value: ${godown_a.get_inventory_value():.2f}")

    print("\n--- Godown B Inventory ---")
    for item in godown_b.inventory.values():
        print(item)
    print(f"Godown B Current Stock: {godown_b.get_current_stock_count()}")
    print(f"Godown B Inventory Value: ${godown_b.get_inventory_value():.2f}")

    # Remove some products from godown A
    print("\n--- Removing products from Godown A ---")
    godown_a.remove_product_from_inventory("P001", 10)
    godown_a.remove_product_from_inventory("P002", 250) # Not enough stock

    print("\n--- Godown A Inventory After Removal ---")
    for item in godown_a.inventory.values():
        print(item)

    # Transfer products
    print("\n--- Transferring products ---")
    system.transfer_product("P001", 5, "G001", "G002")
    system.transfer_product("P003", 50, "G001", "G002") # Not enough stock in G001

    print("\n--- Godown A Inventory After Transfer ---")
    for item in godown_a.inventory.values():
        print(item)

    print("\n--- Godown B Inventory After Transfer ---")
    for item in godown_b.inventory.values():
        print(item)

    print(f"\nTotal System Inventory Value: ${system.get_total_inventory_value_system():.2f}")