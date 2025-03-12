import json

# File handling
def load_library(filename="library.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library, filename="library.json"):
    with open(filename, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library):
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = input("Enter publication year: ")
    genre = input("Enter genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    
    book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
    library.append(book)
    save_library(library)
    print("Book added successfully!\n")

def remove_book(library):
    title = input("Enter the title of the book to remove: ")
    
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            print("Book removed successfully!\n")
            return
    print("Book not found.\n")

def search_book(library):
    query = input("Enter book title or author name to search: ").lower()
    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]
    
    if results:
        print("Matching Books:")
        for book in results:
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("No matching books found.\n")

def display_books(library):
    if not library:
        print("Your library is empty.\n")
        return
    
    print("Your Library:")
    for book in library:
        print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    print()

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    
    print(f"Total books: {total_books}")
    print(f"Percentage read: {read_percentage:.2f}%\n")

def main():
    library = load_library()
    
    while True:
        print("\nPersonal Library Manager")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print("Library saved to file. Goodbye!")
            save_library(library)
            break
        else:
            print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    main()
