import json
from abc import ABC, abstractmethod
from typing import Optional

class Employee(ABC):
    def __init__(self, employee_id: str, name: str, department: str):
        self._employee_id = employee_id
        self._name = name
        self._department = department

    @property
    def employee_id(self) -> str:
        return self._employee_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str):
        self._department = value

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    def display_details(self) -> str:
        return f"ID: {self.employee_id}, Name: {self.name}, Dept: {self.department}"

    def to_dict(self) -> dict:
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'type': 'employee'
        }

class FullTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float):
        super().__init__(employee_id, name, department)
        self._monthly_salary = 0.0
        self.monthly_salary = monthly_salary

    @property
    def monthly_salary(self) -> float:
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value: float):
        if value < 0:
            raise ValueError("Monthly salary cannot be negative.")
        self._monthly_salary = value

    def calculate_salary(self) -> float:
        return self.monthly_salary

    def display_details(self) -> str:
        base = super().display_details()
        return f"{base}, Monthly Salary: ${self.monthly_salary:,.2f}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            'monthly_salary': self.monthly_salary,
            'type': 'fulltime'
        })
        return d

class PartTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, hourly_rate: float, hours_worked_per_month: float):
        super().__init__(employee_id, name, department)
        self._hourly_rate = 0.0
        self._hours_worked_per_month = 0.0
        self.hourly_rate = hourly_rate
        self.hours_worked_per_month = hours_worked_per_month

    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float):
        if value < 0:
            raise ValueError("Hourly rate cannot be negative.")
        self._hourly_rate = value

    @property
    def hours_worked_per_month(self) -> float:
        return self._hours_worked_per_month

    @hours_worked_per_month.setter
    def hours_worked_per_month(self, value: float):
        if value < 0:
            raise ValueError("Hours worked per month cannot be negative.")
        self._hours_worked_per_month = value

    def calculate_salary(self) -> float:
        return self.hourly_rate * self.hours_worked_per_month

    def display_details(self) -> str:
        base = super().display_details()
        return f"{base}, Hourly Rate: ${self.hourly_rate:,.2f}, Hours Worked: {self.hours_worked_per_month}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            'hourly_rate': self.hourly_rate,
            'hours_worked_per_month': self.hours_worked_per_month,
            'type': 'parttime'
        })
        return d

class Manager(FullTimeEmployee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float, bonus: float):
        super().__init__(employee_id, name, department, monthly_salary)
        self._bonus = 0.0
        self.bonus = bonus

    @property
    def bonus(self) -> float:
        return self._bonus

    @bonus.setter
    def bonus(self, value: float):
        if value < 0:
            raise ValueError("Bonus cannot be negative.")
        self._bonus = value

    def calculate_salary(self) -> float:
        return super().calculate_salary() + self.bonus

    def display_details(self) -> str:
        base = super().display_details()
        return f"{base}, Bonus: ${self.bonus:,.2f}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            'bonus': self.bonus,
            'type': 'manager'
        })
        return d

class Company:
    def __init__(self, data_file: str = 'employees.json'):
        self._employees = {}
        self._data_file = data_file
        self._load_data()

    def _load_data(self) -> None:
        try:
            with open(self._data_file, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                for data in data_list:
                    emp_type = data.get('type')
                    try:
                        if emp_type == 'fulltime':
                            emp = FullTimeEmployee(
                                employee_id=data['employee_id'],
                                name=data['name'],
                                department=data['department'],
                                monthly_salary=data['monthly_salary']
                            )
                        elif emp_type == 'parttime':
                            emp = PartTimeEmployee(
                                employee_id=data['employee_id'],
                                name=data['name'],
                                department=data['department'],
                                hourly_rate=data['hourly_rate'],
                                hours_worked_per_month=data['hours_worked_per_month']
                            )
                        elif emp_type == 'manager':
                            emp = Manager(
                                employee_id=data['employee_id'],
                                name=data['name'],
                                department=data['department'],
                                monthly_salary=data['monthly_salary'],
                                bonus=data['bonus']
                            )
                        else:
                            continue
                        self._employees[emp.employee_id] = emp
                    except Exception as e:
                        print(f"Error loading employee: {e}")
                        continue
        except FileNotFoundError:
            self._employees = {}

    def _save_data(self) -> None:
        data_list = [emp.to_dict() for emp in self._employees.values()]
        with open(self._data_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2)

    def add_employee(self, employee: Employee) -> bool:
        if employee.employee_id in self._employees:
            print(f"Employee with ID {employee.employee_id} already exists.")
            return False
        self._employees[employee.employee_id] = employee
        self._save_data()
        print(f"Employee {employee.name} added successfully.")
        return True

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        return self._employees.get(employee_id)

    def update_employee(self, employee_id: str, **kwargs) -> bool:
        employee = self._employees.get(employee_id)
        if not employee:
            print(f"Employee with ID {employee_id} not found.")
            return False

        try:
            for key, value in kwargs.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
                elif key == 'monthly_salary' and isinstance(employee, (FullTimeEmployee, Manager)):
                    employee.monthly_salary = value
                elif key == 'hourly_rate' and isinstance(employee, PartTimeEmployee):
                    employee.hourly_rate = value
                elif key == 'hours_worked_per_month' and isinstance(employee, PartTimeEmployee):
                    employee.hours_worked_per_month = value
                elif key == 'bonus' and isinstance(employee, Manager):
                    employee.bonus = value
                else:
                    print(f"Warning: Attribute '{key}' not found or not applicable for employee ID {employee_id}.")
            self._save_data()
            print(f"Employee {employee_id} updated successfully.")
            return True
        except ValueError as e:
            print(f"Error updating employee {employee_id}: {e}")
            return False

    def delete_employee(self, employee_id: str) -> bool:
        if employee_id in self._employees:
            del self._employees[employee_id]
            self._save_data()
            print(f"Employee {employee_id} deleted successfully.")
            return True
        print(f"Employee with ID {employee_id} not found.")
        return False

    def list_employees(self) -> None:
        if not self._employees:
            print("No employees in the system.")
            return
        print("\n--- Current Employees ---")
        for emp in self._employees.values():
            print(emp.display_details())
        print("-------------------------")

    def calculate_total_payroll(self) -> float:
        total_payroll = sum(emp.calculate_salary() for emp in self._employees.values())
        return total_payroll

def main():
    company = Company()

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. View Employee Details")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. List All Employees")
        print("6. Calculate Total Payroll")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            emp_id = input("Enter Employee ID: ")
            name = input("Enter Name: ")
            department = input("Enter Department: ")
            emp_type = input("Enter Employee Type (fulltime/parttime/manager): ").lower()

            try:
                if emp_type == 'fulltime':
                    monthly_salary = float(input("Enter Monthly Salary: "))
                    emp = FullTimeEmployee(emp_id, name, department, monthly_salary)
                elif emp_type == 'parttime':
                    hourly_rate = float(input("Enter Hourly Rate: "))
                    hours_worked = float(input("Enter Hours Worked Per Month: "))
                    emp = PartTimeEmployee(emp_id, name, department, hourly_rate, hours_worked)
                elif emp_type == 'manager':
                    monthly_salary = float(input("Enter Monthly Salary: "))
                    bonus = float(input("Enter Bonus: "))
                    emp = Manager(emp_id, name, department, monthly_salary, bonus)
                else:
                    print("Invalid employee type.")
                    continue
                company.add_employee(emp)
            except ValueError as e:
                print(f"Invalid input: {e}")

        elif choice == '2':
            emp_id = input("Enter Employee ID to view: ")
            emp = company.get_employee(emp_id)
            if emp:
                print("\n--- Employee Details ---")
                print(emp.display_details())
                print("------------------------")
            else:
                print("Employee not found.")

        elif choice == '3':
            emp_id = input("Enter Employee ID to update: ")
            updates = {}
            while True:
                key = input("Enter attribute to update (e.g., department, monthly_salary, bonus) or 'done' to finish: ")
                if key == 'done':
                    break
                value = input(f"Enter new value for {key}: ")
                try:
                    if key in ['monthly_salary', 'hourly_rate', 'hours_worked_per_month', 'bonus']:
                        updates[key] = float(value)
                    else:
                        updates[key] = value
                except ValueError:
                    print("Invalid value type. Please enter a number for salary/rate/hours/bonus.")
                    continue
            if updates:
                company.update_employee(emp_id, **updates)

        elif choice == '4':
            emp_id = input("Enter Employee ID to delete: ")
            company.delete_employee(emp_id)

        elif choice == '5':
            company.list_employees()

        elif choice == '6':
            total_payroll = company.calculate_total_payroll()
            print(f"\nTotal Monthly Payroll: ${total_payroll:,.2f}")

        elif choice == '7':
            print("Exiting Employee Management System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


    def remove_employee(self, employee_id: str) -> bool:
        if employee_id in self._employees:
            del self._employees[employee_id]
            self._save_data()
            return True
        return False

    def find_employee(self, employee_id: str) -> Optional[Employee]:
        return self._employees.get(employee_id)

    def search_employees_by_name(self, name: str) -> list:
        name_lower = name.lower()
        return [emp for emp in self._employees.values() if name_lower in emp.name.lower()]

    def calculate_total_payroll(self) -> float:
        return sum(emp.calculate_salary() for emp in self._employees.values())

    def display_all_employees(self) -> None:
        if not self._employees:
            print("No employees found.")
            return
        for emp in self._employees.values():
            print(emp.display_details())

    def generate_payroll_report(self) -> None:
        print("Payroll Report:")
        print("-" * 60)
        print(f"{'ID':<12} {'Name':<25} {'Type':<10} {'Salary':>10}")
        print("-" * 60)
        for emp in self._employees.values():
            emp_type = emp.to_dict().get('type', 'Unknown').capitalize()
            salary = emp.calculate_salary()
            print(f"{emp.employee_id:<12} {emp.name:<25} {emp_type:<10} ${salary:>10,.2f}")
        print("-" * 60)
        total_payroll = self.calculate_total_payroll()
        print(f"{'Total Payroll:':<49} ${total_payroll:>10,.2f}")

def main():
    company = Company()

    menu = """
Employee Management System
--------------------------
1. Add Employee
2. Remove Employee
3. View All Employees
4. Search Employee by ID
5. Search Employees by Name
6. Calculate Total Payroll
7. Generate Payroll Report
8. Exit
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-8): ").strip()
        if choice == '1':
            add_employee_interactive(company)
        elif choice == '2':
            employee_id = input("Enter Employee ID to remove: ").strip()
            if company.remove_employee(employee_id):
                print("Employee removed successfully.")
            else:
                print("Employee not found.")
        elif choice == '3':
            company.display_all_employees()
        elif choice == '4':
            employee_id = input("Enter Employee ID to search: ").strip()
            emp = company.find_employee(employee_id)
            if emp:
                print(emp.display_details())
            else:
                print("Employee not found.")
        elif choice == '5':
            name = input("Enter name to search: ").strip()
            matches = company.search_employees_by_name(name)
            if matches:
                print(f"{len(matches)} employee(s) found:")
                for emp in matches:
                    print(emp.display_details())
            else:
                print("No employees found with that name.")
        elif choice == '6':
            total = company.calculate_total_payroll()
            print(f"Total Payroll: ${total:,.2f}")
        elif choice == '7':
            company.generate_payroll_report()
        elif choice == '8':
            print("Exiting Employee Management System. Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

def add_employee_interactive(company: Company):
    print("Select Employee Type to Add:")
    print("1. Full-Time Employee")
    print("2. Part-Time Employee")
    print("3. Manager")
    emp_type_choice = input("Enter choice (1-3): ").strip()
    if emp_type_choice not in ('1', '2', '3'):
        print("Invalid choice.")
        return

    employee_id = input("Enter Employee ID: ").strip()
    if company.find_employee(employee_id):
        print("Employee ID already exists. Cannot add employee.")
        return

    name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()

    try:
        if emp_type_choice == '1':
            monthly_salary = float(input("Enter Monthly Salary: ").strip())
            emp = FullTimeEmployee(employee_id, name, department, monthly_salary)
        elif emp_type_choice == '2':
            hourly_rate = float(input("Enter Hourly Rate: ").strip())
            hours_worked = float(input("Enter Hours Worked per Month: ").strip())
            emp = PartTimeEmployee(employee_id, name, department, hourly_rate, hours_worked)
        else:
            monthly_salary = float(input("Enter Monthly Salary: ").strip())
            bonus = float(input("Enter Monthly Bonus: ").strip())
            emp = Manager(employee_id, name, department, monthly_salary, bonus)
    except ValueError:
        print("Invalid numeric input. Employee not added.")
        return
    except Exception as e:
        print(f"Error creating employee: {e}")
        return

    if company.add_employee(emp):
        print("Employee added successfully.")
    else:
        print("Failed to add employee.")

if __name__ == "_main_":
    main()