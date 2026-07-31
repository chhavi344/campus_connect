import streamlit as st
import os
from database import get_connection

st.set_page_config(
    page_title="Book Exchange",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Book Exchange")
st.caption("Share and Exchange Books with Students")

# login check
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# DELETE FUNCTION

def delete_book(book_id, user_id):
    """Delete a book only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this book
        cursor.execute(
            "SELECT user_id FROM books WHERE book_id = %s",
            (book_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the book
            cursor.execute(
                "DELETE FROM books WHERE book_id = %s AND user_id = %s",
                (book_id, user_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
    except Exception as e:
        st.error(f"Error deleting book: {e}")
        return False


# CREATE UPLOAD FOLDER

UPLOAD_FOLDER = "uploads/books"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# UPLOAD BOOK

st.subheader("📚 Upload Book")

book_name = st.text_input("Book Name")
author = st.text_input("Author Name")
subject = st.text_input("Subject")
condition = st.selectbox(
    "Book Condition",
    [
        "Excellent",
        "Good",
        "Average",
        "Old"
    ]
)
description = st.text_area("Description")
image = st.file_uploader(
    "Upload Book Image",
    type=["jpg","jpeg","png"]
)

if st.button("Upload Book", use_container_width=True):

    if book_name.strip()=="":
        st.error("Enter Book Name")
    elif author.strip()=="":
        st.error("Enter Author Name")
    elif subject.strip()=="":
        st.error("Enter Subject")
    elif description.strip()=="":
        st.error("Enter Description")
    else:
        image_path=""
        if image is not None:
            image_path=os.path.join(UPLOAD_FOLDER, image.name)
            with open(image_path,"wb") as f:
                f.write(image.getbuffer())

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute(
            """
            INSERT INTO books
            (user_id, book_name, author, subject, book_condition, description, image_path)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state.get("user_id"),
                book_name,
                author,
                subject,
                condition,
                description,
                image_path
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("📚 Book Uploaded Successfully")
        st.rerun()

st.divider()


# ALL BOOKS WITH DELETE BUTTON
st.subheader("📚 Available Books")

search = st.text_input(
    "🔍 Search Books",
    placeholder="Search by Book Name or Subject"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        b.*,
        u.full_name,
        u.user_id as owner_id
    FROM books b
    LEFT JOIN users u
    ON b.user_id = u.user_id
    WHERE
        b.book_name LIKE %s
        OR
        b.subject LIKE %s
    ORDER BY b.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    )
)

books = cursor.fetchall()
cursor.close()
conn.close()

if len(books) == 0:
    if search.strip() != "":
        st.error("❌ Book Not Found")
    else:
        st.info("No Books Available")
else:
    for book in books:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if book["image_path"]:
                    if os.path.exists(book["image_path"]):
                        st.image(book["image_path"], width=150)

            with col2:
                st.subheader(book["book_name"])
                st.write("✍ Author :", book["author"])
                st.write("📘 Subject :", book["subject"])
                st.write("⭐ Condition :", book["book_condition"])
                st.write("📦 Status :", book["status"])
                st.write("📝 Description :")
                st.write(book["description"])
                
                # Show who uploaded
                st.caption(f"👤 Uploaded By: {book['full_name']}")

            with col3:
                
                # DELETE BUTTON - Only for post owner
                
                if st.session_state.get('user_id') == book['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_book_{book['book_id']}",
                        use_container_width=True
                    ):
                        if delete_book(book['book_id'], st.session_state['user_id']):
                            st.success("✅ Book deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete book")
                else:
                    st.info("🔒 Post by other user")

st.divider()


# NAVIGATION BUTTONS

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()
st.caption("📚 CampusConnect | Book Exchange")