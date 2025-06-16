import datetime

class Person:
    def __init__(self, person_id, name, contact_info):
        self.person_id = person_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"ID: {self.person_id}, Name: {self.name}, Contact: {self.contact_info}"

class Passenger(Person):
    def __init__(self, person_id, name, contact_info, passport_number):
        super().__init__(person_id, name, contact_info)
        self.passport_number = passport_number
        self.bookings = []

    def add_booking(self, flight):
        self.bookings.append(flight)

    def __str__(self):
        return f"Passenger - {super().__str__()}, Passport: {self.passport_number}"

class Employee(Person):
    def __init__(self, person_id, name, contact_info, employee_id, role):
        super().__init__(person_id, name, contact_info)
        self.employee_id = employee_id
        self.role = role

    def __str__(self):
        return f"Employee - {super().__str__()}, Employee ID: {self.employee_id}, Role: {self.role}"

class Flight:
    def __init__(self, flight_number, origin, destination, departure_time, arrival_time, capacity):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time # datetime object
        self.arrival_time = arrival_time     # datetime object
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            passenger.add_booking(self)
            print(f"Passenger {passenger.name} added to flight {self.flight_number}.")
            return True
        else:
            print(f"Flight {self.flight_number} is full.")
            return False

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            print(f"Passenger {passenger.name} removed from flight {self.flight_number}.")
            return True
        else:
            print(f"Passenger {passenger.name} not found on flight {self.flight_number}.")
            return False

    def get_available_seats(self):
        return self.capacity - len(self.passengers)

    def __str__(self):
        return (f"Flight {self.flight_number}: {self.origin} to {self.destination} | "
                f"Departure: {self.departure_time.strftime('%Y-%m-%d %H:%M')} | "
                f"Arrival: {self.arrival_time.strftime('%Y-%m-%d %H:%M')} | "
                f"Seats: {self.get_available_seats()}/{self.capacity}")

class Airport:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.flights = {}
        self.passengers = {}
        self.employees = {}

    def add_flight(self, flight):
        if flight.flight_number not in self.flights:
            self.flights[flight.flight_number] = flight
            print(f"Flight {flight.flight_number} added to {self.name} Airport.")
        else:
            print(f"Flight {flight.flight_number} already exists.")

    def add_passenger(self, passenger):
        if passenger.person_id not in self.passengers:
            self.passengers[passenger.person_id] = passenger
            print(f"Passenger {passenger.name} added to {self.name} Airport.")
        else:
            print(f"Passenger {passenger.name} already registered.")

    def add_employee(self, employee):
        if employee.person_id not in self.employees:
            self.employees[employee.person_id] = employee
            print(f"Employee {employee.name} added to {self.name} Airport.")
        else:
            print(f"Employee {employee.name} already registered.")

    def get_flight(self, flight_number):
        return self.flights.get(flight_number)

    def get_passenger(self, passenger_id):
        return self.passengers.get(passenger_id)

    def get_employee(self, employee_id):
        return self.employees.get(employee_id)

    def search_flights(self, origin=None, destination=None, date=None):
        found_flights = []
        for flight in self.flights.values():
            match = True
            if origin and flight.origin != origin:
                match = False
            if destination and flight.destination != destination:
                match = False
            if date and flight.departure_time.date() != date:
                match = False
            if match:
                found_flights.append(flight)
        return found_flights

    def __str__(self):
        return (f"Airport: {self.name} ({self.code}) | "
                f"Flights: {len(self.flights)} | "
                f"Passengers: {len(self.passengers)} | "
                f"Employees: {len(self.employees)}")

# Example Usage:
if __name__ == "__main__":
    # Create an airport
    lax_airport = Airport("Los Angeles International Airport", "LAX")
    print(lax_airport)

    # Add employees
    emp1 = Employee("E001", "John Doe", "john.doe@airport.com", "EMP001", "Ground Staff")
    emp2 = Employee("E002", "Jane Smith", "jane.smith@airport.com", "EMP002", "Air Traffic Controller")
    lax_airport.add_employee(emp1)
    lax_airport.add_employee(emp2)

    # Add passengers
    pax1 = Passenger("P001", "Alice Wonderland", "alice@example.com", "AB12345")
    pax2 = Passenger("P002", "Bob The Builder", "bob@example.com", "CD67890")
    lax_airport.add_passenger(pax1)
    lax_airport.add_passenger(pax2)

    # Define flights
    flight1_dep = datetime.datetime(2024, 7, 20, 10, 0)
    flight1_arr = datetime.datetime(2024, 7, 20, 12, 0)
    flight1 = Flight("AA101", "LAX", "JFK", flight1_dep, flight1_arr, 150)

    flight2_dep = datetime.datetime(2024, 7, 20, 14, 0)
    flight2_arr = datetime.datetime(2024, 7, 20, 16, 30)
    flight2 = Flight("UA202", "LAX", "SFO", flight2_dep, flight2_arr, 100)

    lax_airport.add_flight(flight1)
    lax_airport.add_flight(flight2)

    # Add passengers to flights
    flight1.add_passenger(pax1)
    flight1.add_passenger(pax2)

    # Search flights
    print("\n--- Searching Flights ---")
    today = datetime.date(2024, 7, 20)
    flights_to_jfk = lax_airport.search_flights(destination="JFK", date=today)
    for f in flights_to_jfk:
        print(f)

    # Display flight details
    print("\n--- Flight Details ---")
    print(flight1)
    print(flight2)

    # Display passenger bookings
    print("\n--- Passenger Bookings ---")
    for booking in pax1.bookings:
        print(f"Alice has a booking on: {booking.flight_number}")

    # Remove passenger from flight
    flight1.remove_passenger(pax2)
    print("\n--- Flight 1 after passenger removal ---")
    print(flight1)