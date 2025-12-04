import json
from pathlib import Path
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | {self.isbn} | {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"
class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_catalog()

    def add_book(self, book):
        self.books.append(book)
        self.save_catalog()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books

    def save_catalog(self):
        try:
            data = [b.to_dict() for b in self.books]
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        except:
            print("Error saving file.")

    def load_catalog(self):
        try:
            if not self.file_path.exists():
                return
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        except:
            print("Error loading file. Starting with empty catalog.")
            self.books = []
def menu():
    print("\n--- Library Menu ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")


def main():
    inventory = LibraryInventory()

    while True:
        menu()
        choice = input("Enter option: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            inventory.add_book(Book(title, author, isbn))

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.issue():
                print("Book issued.")
            else:
                print("Cannot issue.")
            inventory.save_catalog()

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.return_book():
                print("Book returned.")
            else:
                print("Cannot return.")
            inventory.save_catalog()

        elif choice == "4":
            for b in inventory.display_all():
                print(b)

        elif choice == "5":
            title = input("Enter title to search: ")
            results = inventory.search_by_title(title)
            if results:
                for b in results:
                    print(b)
            else:
                print("No books found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()