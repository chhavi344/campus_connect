import streamlit as st
import os
from database import get_connection

st.set_page_config(
    page_title="Notes Sharing",
    page_icon="📚",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

st.title("📚 Notes Sharing")
st.caption("Upload and Share Notes with Students")

st.divider()

UPLOAD_FOLDER = "uploads/notes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# DELETE FUNCTION

def delete_note(note_id, user_id):
    """Delete a note only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First get the pdf path to delete the file
        cursor.execute(
            "SELECT user_id, pdf_path FROM notes WHERE note_id = %s",
            (note_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the PDF file
            pdf_path = result[1]
            if pdf_path and os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                except:
                    pass  # File delete failed, but continue
            
            # Delete from database
            cursor.execute(
                "DELETE FROM notes WHERE note_id = %s AND user_id = %s",
                (note_id, user_id)
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
        st.error(f"Error deleting note: {e}")
        return False


# UPLOAD NOTES

st.subheader("📤 Upload Notes")

title = st.text_input("📖 Notes Title")
subject = st.text_input("📘 Subject")
semester = st.selectbox(
    "📚 Semester",
    [
        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6",
        "Semester 7",
        "Semester 8"
    ]
)
description = st.text_area("📝 Description")
pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])

if st.button("📤 Upload Notes", use_container_width=True):
    if title.strip() == "":
        st.error("Please Enter Notes Title")
    elif subject.strip() == "":
        st.error("Please Enter Subject")
    elif description.strip() == "":
        st.error("Please Enter Description")
    elif pdf is None:
        st.error("Please Upload PDF")
    else:
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.name)
        with open(pdf_path, "wb") as f:
            f.write(pdf.getbuffer())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO notes
            (user_id, title, subject, semester, description, pdf_path)
            VALUES(%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state["user_id"],
                title,
                subject,
                semester,
                description,
                pdf_path
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Notes Uploaded Successfully")
        st.balloons()
        st.rerun()

st.divider()

# ALL NOTES WITH DELETE BUTTON

st.subheader("📚 All Shared Notes")

search = st.text_input(
    "🔍 Search Notes",
    placeholder="Search by Title or Subject"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

if search.strip() == "":
    cursor.execute("""
        SELECT
            notes.*,
            users.full_name,
            users.user_id as owner_id
        FROM notes
        JOIN users
        ON notes.user_id = users.user_id
        ORDER BY created_at DESC
    """)
else:
    cursor.execute("""
        SELECT
            notes.*,
            users.full_name,
            users.user_id as owner_id
        FROM notes
        JOIN users
        ON notes.user_id = users.user_id
        WHERE
            title LIKE %s
            OR subject LIKE %s
        ORDER BY created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    ))

notes = cursor.fetchall()
cursor.close()
conn.close()

if len(notes) == 0:
    st.info("No Notes Found.")
else:
    for note in notes:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader(note["title"])
                st.write("📘 Subject :", note["subject"])
                st.write("📚 Semester :", note["semester"])
                st.write("👤 Uploaded By :", note["full_name"])
                st.write("📝 Description :")
                st.write(note["description"])

            with col2:
                if os.path.exists(note["pdf_path"]):
                    with open(note["pdf_path"], "rb") as pdf_file:
                        st.download_button(
                            "⬇ Download PDF",
                            data=pdf_file,
                            file_name=os.path.basename(note["pdf_path"]),
                            mime="application/pdf",
                            key=f"download_{note['note_id']}"
                        )
                else:
                    st.error("PDF File Not Found")

            with col3:
            
                # DELETE BUTTON 
                if st.session_state.get('user_id') == note['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_note_{note['note_id']}",
                        use_container_width=True
                    ):
                        if delete_note(note['note_id'], st.session_state['user_id']):
                            st.success("✅ Note deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete note")
                else:
                    st.info("🔒 Uploaded by other user")

        st.write("")
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
st.caption("📚 CampusConnect | Notes Sharing")