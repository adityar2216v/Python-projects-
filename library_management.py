import json
from datetime import datetime, timedelta
from typing import List, Optional

class Book:
    def __init__(self, title: str, author: str, isbn: str, publication_year: int, quantity: int):
        if not all([title, author, isbn, publication_year, quantity is not None]):
            raise ValueError("All book fields must be provided.")
        if not isinstance(publication_year, int) or publication_year <= 0:
            raise ValueError("Publication year must be a positive integer.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.quantity = quantity
        self.available_copies = quantity

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Available: {self.available_copies}/{self.quantity}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "quantity": self.quantity,
            "available_copies": self.available_copies
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['title'], data['author'], data['isbn'], data['publication_year'], data['quantity'])

class Member:
    def __init__(self, member_id: str, name: str, email: str):
        if not all([member_id, name, email]):
            raise ValueError("All member fields must be provided.")
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = [] # List of (isbn, borrow_date)

    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Email: {self.email}"

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data: dict):
        member = cls(data['member_id'], data['name'], data['email'])
        member.borrowed_books = data.get('borrowed_books', [])
        return member

class Library:
    def __init__(self, data_file: str = 'library_data.json'):
        self.books = {}
        self.members = {}
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for isbn, book_data in data.get('books', {}).items():
                    book = Book.from_dict(book_data)
                    self.books[isbn] = book
                for member_id, member_data in data.get('members', {}).items():
                    member = Member.from_dict(member_data)
                    self.members[member_id] = member
        except FileNotFoundError:
            pass # No data file yet, start with empty library
        except json.JSONDecodeError:
            print("Error decoding JSON from data file. Starting with empty library.")

    def _save_data(self):
        data = {
            "books": {isbn: book.to_dict() for isbn, book in self.books.items()},
            "members": {member_id: member.to_dict() for member_id, member in self.members.items()}
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def add_book(self, book: Book) -> bool:
        if book.isbn in self.books:
            print(f"Book with ISBN {book.isbn} already exists. Updating quantity.")
            self.books[book.isbn].quantity += book.quantity
            self.books[book.isbn].available_copies += book.quantity
            self._save_data()
            return True
        self.books[book.isbn] = book
        self._save_data()
        print(f"Book '{book.title}' added to the library.")
        return True

    def remove_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            print(f"Book with ISBN {isbn} not found.")
            return False
        if any(isbn == borrowed_isbn for member in self.members.values() for borrowed_isbn, _ in member.borrowed_books):
            print(f"Cannot remove book {isbn}. It is currently borrowed by one or more members.")
            return False
        del self.books[isbn]
        self._save_data()
        print(f"Book with ISBN {isbn} removed from the library.")
        return True

    def register_member(self, member: Member) -> bool:
        if member.member_id in self.members:
            print(f"Member with ID {member.member_id} already registered.")
            return False
        self.members[member.member_id] = member
        self._save_data()
        print(f"Member '{member.name}' registered successfully.")
        return True

    def unregister_member(self, member_id: str) -> bool:
        if member_id not in self.members:
            print(f"Member with ID {member_id} not found.")
            return False
        if self.members[member_id].borrowed_books:
            print(f"Cannot unregister member {member_id}. They still have borrowed books.")
            return False
        del self.members[member_id]
        self._save_data()
        print(f"Member with ID {member_id} unregistered.")
        return True

    def borrow_book(self, isbn: str, member_id: str) -> bool:
        book = self.books.get(isbn)
        member = self.members.get(member_id)

        if not book:
            print(f"Book with ISBN {isbn} not found.")
            return False
        if not member:
            print(f"Member with ID {member_id} not found.")
            return False
        if book.available_copies <= 0:
            print(f"No available copies of '{book.title}'.")
            return False
        if any(isbn == borrowed_isbn for borrowed_isbn, _ in member.borrowed_books):
            print(f"Member {member.name} has already borrowed '{book.title}'.")
            return False

        book.available_copies -= 1
        member.borrowed_books.append((isbn, datetime.now().isoformat()))
        self._save_data()
        print(f"'{book.title}' borrowed by {member.name} successfully.")
        return True

    def return_book(self, isbn: str, member_id: str) -> bool:
        book = self.books.get(isbn)
        member = self.members.get(member_id)

        if not book:
            print(f"Book with ISBN {isbn} not found.")
            return False
        if not member:
            print(f"Member with ID {member_id} not found.")
            return False

        try:
            # Find and remove the specific borrowed book entry
            borrowed_entry_index = -1
            for i, (borrowed_isbn, _) in enumerate(member.borrowed_books):
                if borrowed_isbn == isbn:
                    borrowed_entry_index = i
                    break
            
            if borrowed_entry_index == -1:
                print(f"Member {member.name} did not borrow '{book.title}'.")
                return False

            member.borrowed_books.pop(borrowed_entry_index)
            book.available_copies += 1
            self._save_data()
            print(f"'{book.title}' returned by {member.name} successfully.")
            return True
        except ValueError:
            print(f"Member {member.name} did not borrow '{book.title}'.")
            return False

    def search_book(self, query: str, search_by: str = 'title') -> List[Book]:
        results = []
        query_lower = query.lower()
        for book in self.books.values():
            if search_by == 'title' and query_lower in book.title.lower():
                results.append(book)
            elif search_by == 'author' and query_lower in book.author.lower():
                results.append(book)
            elif search_by == 'isbn' and query_lower == book.isbn.lower():
                results.append(book)
        return results

    def list_all_books(self):
        if not self.books:
            print("No books in the library.")
            return
        print("\n--- All Books ---")
        for book in self.books.values():
            print(book)
        print("-------------------")

    def list_all_members(self):
        if not self.members:
            print("No members registered.")
            return
        print("\n--- All Members ---")
        for member in self.members.values():
            print(member)
            if member.borrowed_books:
                print("  Borrowed Books:")
                for isbn, borrow_date_str in member.borrowed_books:
                    borrow_date = datetime.fromisoformat(borrow_date_str)
                    book_title = self.books[isbn].title if isbn in self.books else "Unknown Book"
                    print(f"    - '{book_title}' (ISBN: {isbn}) borrowed on {borrow_date.strftime('%Y-%m-%d')}")
            else:
                print("  No books borrowed.")
        print("---------------------")

def get_valid_input(prompt: str, type_func=str, error_message: str = "Invalid input. Please try again."):
    while True:
        try:
            return type_func(input(prompt).strip())
        except ValueError:
            print(error_message)

def main():
    library = Library()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Register Member")
        print("4. Unregister Member")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Search Books")
        print("8. List All Books")
        print("9. List All Members")
        print("10. Exit")

        choice = get_valid_input("Enter your choice: ", int)

        if choice == 1:
            title = get_valid_input("Enter book title: ")
            author = get_valid_input("Enter book author: ")
            isbn = get_valid_input("Enter book ISBN: ")
            try:
                pub_year = get_valid_input("Enter publication year: ", int)
                quantity = get_valid_input("Enter quantity: ", int)
                book = Book(title, author, isbn, pub_year, quantity)
                library.add_book(book)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 2:
            isbn = get_valid_input("Enter ISBN of book to remove: ")
            library.remove_book(isbn)

        elif choice == 3:
            member_id = get_valid_input("Enter member ID: ")
            name = get_valid_input("Enter member name: ")
            email = get_valid_input("Enter member email: ")
            try:
                member = Member(member_id, name, email)
                library.register_member(member)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 4:
            member_id = get_valid_input("Enter member ID to unregister: ")
            library.unregister_member(member_id)

        elif choice == 5:
            isbn = get_valid_input("Enter ISBN of book to borrow: ")
            member_id = get_valid_input("Enter member ID: ")
            library.borrow_book(isbn, member_id)

        elif choice == 6:
            isbn = get_valid_input("Enter ISBN of book to return: ")
            member_id = get_valid_input("Enter member ID: ")
            library.return_book(isbn, member_id)

        elif choice == 7:
            search_by = get_valid_input("Search by (title/author/isbn): ").lower()
            if search_by not in ['title', 'author', 'isbn']:
                print("Invalid search criteria. Please choose 'title', 'author', or 'isbn'.")
                continue
            query = get_valid_input(f"Enter {search_by} to search for: ")
            results = library.search_book(query, search_by)
            if results:
                print("\n--- Search Results ---")
                for book in results:
                    print(book)
                print("----------------------")
            else:
                print("No books found matching your query.")

        elif choice == 8:
            library.list_all_books()

        elif choice == 9:
            library.list_all_members()

        elif choice == 10:
            print("Exiting Library Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()