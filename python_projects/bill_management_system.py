import datetime

class Bill:
    def __init__(self, bill_id, customer_id, amount, due_date, description=""):
        self.bill_id = bill_id
        self.customer_id = customer_id
        self.amount = amount
        self.due_date = due_date  # datetime.date object
        self.description = description
        self.is_paid = False
        self.payment_date = None

    def mark_as_paid(self):
        if not self.is_paid:
            self.is_paid = True
            self.payment_date = datetime.date.today()
            print(f"Bill {self.bill_id} marked as paid on {self.payment_date}.")
        else:
            print(f"Bill {self.bill_id} is already paid.")

    def __str__(self):
        status = "Paid" if self.is_paid else "Unpaid"
        payment_info = f", Paid Date: {self.payment_date}" if self.payment_date else ""
        return (f"Bill ID: {self.bill_id}, Customer ID: {self.customer_id}, "
                f"Amount: ${self.amount:.2f}, Due Date: {self.due_date}, "
                f"Status: {status}{payment_info}, Description: {self.description}")

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.bills = []

    def add_bill(self, bill):
        self.bills.append(bill)

    def get_unpaid_bills(self):
        return [bill for bill in self.bills if not bill.is_paid]

    def get_paid_bills(self):
        return [bill for bill in self.bills if bill.is_paid]

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"

class BillManager:
    def __init__(self):
        self.bills = {}
        self.customers = {}

    def add_customer(self, customer):
        if customer.customer_id not in self.customers:
            self.customers[customer.customer_id] = customer
            print(f"Customer {customer.name} added.")
        else:
            print(f"Customer {customer.name} already exists.")

    def create_bill(self, customer_id, amount, due_date, description=""):
        if customer_id in self.customers:
            bill_id = f"B{len(self.bills) + 1:04d}"
            bill = Bill(bill_id, customer_id, amount, due_date, description)
            self.bills[bill_id] = bill
            self.customers[customer_id].add_bill(bill)
            print(f"Bill {bill_id} created for customer {customer_id}.")
            return bill
        else:
            print(f"Customer {customer_id} not found.")
            return None

    def get_bill(self, bill_id):
        return self.bills.get(bill_id)

    def get_customer(self, customer_id):
        return self.customers.get(customer_id)

    def mark_bill_as_paid(self, bill_id):
        bill = self.get_bill(bill_id)
        if bill:
            bill.mark_as_paid()
        else:
            print(f"Bill {bill_id} not found.")

    def get_all_unpaid_bills(self):
        return [bill for bill in self.bills.values() if not bill.is_paid]

    def get_all_paid_bills(self):
        return [bill for bill in self.bills.values() if bill.is_paid]

    def get_bills_by_customer(self, customer_id):
        customer = self.get_customer(customer_id)
        if customer:
            return customer.bills
        else:
            print(f"Customer {customer_id} not found.")
            return []

# Example Usage:
if __name__ == "__main__":
    manager = BillManager()

    # Add customers
    cust1 = Customer("C001", "Alice Johnson", "alice@example.com")
    cust2 = Customer("C002", "Bob Williams", "bob@example.com")
    manager.add_customer(cust1)
    manager.add_customer(cust2)

    # Create bills
    bill1 = manager.create_bill("C001", 100.50, datetime.date(2024, 8, 1), "Monthly Subscription")
    bill2 = manager.create_bill("C001", 50.00, datetime.date(2024, 7, 15), "One-time Service Fee")
    bill3 = manager.create_bill("C002", 250.75, datetime.date(2024, 8, 10), "Annual Membership")
    bill4 = manager.create_bill("C001", 75.20, datetime.date(2024, 9, 1), "Consultation Fee")

    print("\n--- All Bills ---")
    for bill_id, bill in manager.bills.items():
        print(bill)

    # Mark a bill as paid
    print("\n--- Marking Bill B0001 as Paid ---")
    manager.mark_bill_as_paid("B0001")
    print(manager.get_bill("B0001"))

    # Get unpaid bills for a customer
    print("\n--- Alice's Unpaid Bills ---")
    alice_unpaid_bills = cust1.get_unpaid_bills()
    for bill in alice_unpaid_bills:
        print(bill)

    # Get all unpaid bills in the system
    print("\n--- All Unpaid Bills in System ---")
    all_unpaid = manager.get_all_unpaid_bills()
    for bill in all_unpaid:
        print(bill)

    # Get all paid bills in the system
    print("\n--- All Paid Bills in System ---")
    all_paid = manager.get_all_paid_bills()
    for bill in all_paid:
        print(bill)

    # Get all bills for a customer
    print("\n--- Bob's All Bills ---")
    bob_bills = manager.get_bills_by_customer("C002")
    for bill in bob_bills:
        print(bill)