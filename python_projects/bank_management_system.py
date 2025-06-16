class Account:
    def __init__(self, account_number, account_holder, balance=0):
        self.transactions = []
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +{amount} (New balance: {self.balance})")
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transactions.append(f"Withdrawal: -{amount} (New balance: {self.balance})")
                print(f"Withdrew {amount}. New balance: {self.balance}")
            else:
                print("Insufficient balance.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

    def __str__(self):
        return f"Account No: {self.account_number}, Holder: {self.account_holder}, Balance: {self.balance}"

class Customer:
    def __init__(self, customer_id, name, address):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
        print(f"Account {account.account_number} added for customer {self.name}.")

    def get_accounts(self):
        return self.accounts

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Address: {self.address}"

class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = {}
        self.accounts = {}
        self.next_account_number = 1001

    def add_customer(self, customer):
        if customer.customer_id not in self.customers:
            self.customers[customer.customer_id] = customer
            print(f"Customer {customer.name} added to {self.name}.")
        else:
            print(f"Customer with ID {customer.customer_id} already exists.")

    def create_account(self, customer_id, initial_balance=0):
        if customer_id in self.customers:
            account_number = self.next_account_number
            self.next_account_number += 1
            account = Account(account_number, self.customers[customer_id].name, initial_balance)
            self.accounts[account_number] = account
            self.customers[customer_id].add_account(account)
            print(f"Account {account_number} created for customer {self.customers[customer_id].name}.")
            return account
        else:
            print(f"Customer with ID {customer_id} not found.")
            return None

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def get_customer(self, customer_id):
        return self.customers.get(customer_id)

    def remove_customer(self, customer_id):
        if customer_id in self.customers:
            customer = self.customers.pop(customer_id)
            # Remove all accounts associated with this customer
            accounts_to_remove = [acc.account_number for acc in customer.get_accounts()]
            for acc_num in accounts_to_remove:
                if acc_num in self.accounts:
                    del self.accounts[acc_num]
            print(f"Customer {customer.name} and all associated accounts removed from {self.name}.")
        else:
            print(f"Customer with ID {customer_id} not found.")

    def transfer_funds(self, from_account_num, to_account_num, amount):
        from_account = self.get_account(from_account_num)
        to_account = self.get_account(to_account_num)

        if not from_account:
            print(f"Source account {from_account_num} not found.")
            return
        if not to_account:
            print(f"Destination account {to_account_num} not found.")
            return
        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        if from_account.get_balance() >= amount:
            from_account.withdraw(amount)
            to_account.deposit(amount)
            print(f"Successfully transferred {amount} from {from_account_num} to {to_account_num}.")
        else:
            print(f"Insufficient balance in account {from_account_num} for transfer.")

    def __str__(self):
        return f"Bank: {self.name}, Customers: {len(self.customers)}, Accounts: {len(self.accounts)}"

# Example Usage:
if __name__ == "__main__":
    my_bank = Bank("My Awesome Bank")

    # Add customers
    customer1 = Customer("C001", "Alice Smith", "123 Main St")
    customer2 = Customer("C002", "Bob Johnson", "456 Oak Ave")

    my_bank.add_customer(customer1)
    my_bank.add_customer(customer2)

    # Create accounts
    account1 = my_bank.create_account("C001", 1000)
    account2 = my_bank.create_account("C002", 500)
    account3 = my_bank.create_account("C001", 200)

    if account1:
        account1.deposit(200)
        account1.withdraw(150)
        print(f"Alice's account balance: {account1.get_balance()}")

    if account2:
        account2.withdraw(600) # Insufficient balance
        account2.deposit(1000)
        print(f"Bob's account balance: {account2.get_balance()}")

    print("\n--- Transaction History for Alice's Account ---")
    if account1:
        for transaction in account1.get_transaction_history():
            print(transaction)

    print("\n--- Fund Transfer ---")
    my_bank.transfer_funds(account1.account_number, account2.account_number, 50)
    print(f"Alice's account balance after transfer: {account1.get_balance()}")
    print(f"Bob's account balance after transfer: {account2.get_balance()}")

    print("\n--- Remove Customer ---")
    my_bank.remove_customer("C001")

    print("\n--- Bank Status After Operations ---")
    print(my_bank)

    print("\n--- Remaining Customer Accounts ---")
    for customer_id, customer in my_bank.customers.items():
        print(customer)
        for acc in customer.get_accounts():
            print(acc)