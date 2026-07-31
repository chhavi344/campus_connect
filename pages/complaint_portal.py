import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Complaint Portal",
    page_icon="🛠",
    layout="wide"
)

st.title("🛠 Complaint Portal")
st.caption("Submit and Track Campus Complaints")

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# DELETE FUNCTION

def delete_complaint(complaint_id, user_id):
    """Delete a complaint only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this complaint
        cursor.execute(
            "SELECT user_id FROM complaints WHERE complaint_id = %s",
            (complaint_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the complaint
            cursor.execute(
                "DELETE FROM complaints WHERE complaint_id = %s AND user_id = %s",
                (complaint_id, user_id)
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
        st.error(f"Error deleting complaint: {e}")
        return False
# SUBMIT COMPLAINT

st.subheader("📝 Submit Complaint")

category = st.selectbox(
    "Category",
    [
        "Electricity",
        "Water",
        "WiFi",
        "Classroom",
        "Hostel",
        "Library",
        "Cleanliness",
        "Other"
    ]
)

title = st.text_input("Complaint Title")
description = st.text_area("Description")

if st.button("Submit Complaint", use_container_width=True):

    if title.strip() == "":
        st.error("Enter Complaint Title")
    elif description.strip() == "":
        st.error("Enter Description")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO complaints
            (user_id, category, title, description)
            VALUES(%s,%s,%s,%s)
            """,
            (
                st.session_state.get("user_id"),
                category,
                title,
                description
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Complaint Submitted Successfully")
        st.balloons()
        st.rerun()

st.divider()


# NAVIGATION BUTTONS

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.divider()


# ALL COMPLAINTS WITH DELETE BUTTON

st.subheader("📋 All Complaints")

search = st.text_input(
    "🔍 Search Complaint",
    placeholder="Search by Title or Category"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        c.*,
        u.full_name,
        u.user_id as owner_id
    FROM complaints c
    LEFT JOIN users u
    ON c.user_id = u.user_id
    WHERE
        c.title LIKE %s
        OR c.category LIKE %s
    ORDER BY c.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    )
)

complaints = cursor.fetchall()
cursor.close()
conn.close()

if len(complaints) == 0:
    if search.strip() != "":
        st.error("❌ Complaint Not Found")
    else:
        st.info("No Complaints Found")
else:
    for complaint in complaints:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"🛠 {complaint['title']}")
                st.write("📂 Category :", complaint["category"])
                st.write("📝 Description :")
                st.write(complaint["description"])
                st.write("📌 Status :", complaint["status"])
                st.write("📅 Date :", complaint["created_at"])
                st.caption(f"👤 Posted By: {complaint['full_name']}")

            with col2:
                
                # DELETE BUTTON - Only for post owner
                
                if st.session_state.get('user_id') == complaint['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_complaint_{complaint['complaint_id']}",
                        use_container_width=True
                    ):
                        if delete_complaint(complaint['complaint_id'], st.session_state['user_id']):
                            st.success("✅ Complaint deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete complaint")
                else:
                    st.info("🔒 Post by other user")

st.divider()


# LOGOUT

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()
st.caption("🛠 CampusConnect | Complaint Portal")