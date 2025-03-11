import streamlit as st
import json
import os
import base64

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

# Directory for storing uploaded files
UPLOAD_FOLDER = "uploaded_books"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit UI
st.title("📚 Personal Library Manager")

library = load_library()

# Sidebar menu with Exit option
menu = st.sidebar.selectbox("Select an option", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Library Statistics", "Exit"])

if menu == "Add a Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    uploaded_file = st.file_uploader("Upload Book File", type=["pdf", "txt"])

    if st.button("Add Book"):
        if title and author and year and genre and uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "file_path": file_path}
            library.append(book)
            save_library(library)
            st.success("Book added successfully!")
        else:
            st.warning("Please fill in all fields and upload a file.")

elif menu == "Remove a Book":
    st.header("Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        title_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != title_to_remove]
            save_library(library)
            st.success("Book removed successfully!")
    else:
        st.warning("No books available to remove.")

elif menu == "Search for a Book":
    st.header("Search for a Book")
    search_query = st.text_input("Enter title or author name")
    if search_query:
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                file_link = f"[📂 Read Book]({book['file_path']})" if book['file_path'] else "No file uploaded"
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'} - {file_link}")
        else:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.header("All Books in Library")
    if library:
        for book in library:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
            with col2:
                if st.button("📖 Read Now", key=book["title"]):
                    st.session_state["selected_book"] = book
                    st.rerun()
    else:
        st.warning("Your library is empty.")

elif menu == "Library Statistics":
    st.header("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"✅ Percentage Read: {read_percentage:.2f}%")

elif menu == "Exit":
    st.header("📤 Exiting the Library")
    st.write("You have exited the library. See you next time! 😊")
    st.session_state.clear()
    st.stop()

# Book Reading View
if "selected_book" in st.session_state:
    book = st.session_state["selected_book"]
    st.header(f"📖 Reading: {book['title']}")

    file_ext = book["file_path"].split(".")[-1]
    
    if file_ext == "pdf":
        with open(book["file_path"], "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700px" height="900px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
    
    elif file_ext == "txt":
        with open(book["file_path"], "r", encoding="utf-8") as f:
            text_content = f.read()
            st.text_area("📜 Book Content", text_content, height=400)
    
    if st.button("Close Book"):
        del st.session_state["selected_book"]
        st.rerun()
