import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Complaint Portal",
    page_icon="🛠",
    layout="wide"
)

st.title("🛠 Complaint Portal")
st.caption("Submit and Track Campus Complaints")

#  LOGIN CHECK 

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

#  SUBMIT COMPLAINT

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

if st.button(
    "Submit Complaint",
    use_container_width=True
):

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
            (
                user_id,
                category,
                title,
                description
            )
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
        
# DASHBOARD BUTTON


st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/dashboard.py")

st.divider()


# ALL COMPLAINTS


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
        u.full_name
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

if len(complaints) == 0:

    if search.strip() != "":
        st.error("❌ Complaint Not Found")

    else:
        st.info("No Complaints Found")

else:

    for complaint in complaints:

        with st.container(border=True):

            st.subheader(complaint["title"])

            st.write("👤 Posted By :", complaint["full_name"])

            st.write("📂 Category :", complaint["category"])

            st.write("📝 Description :")

            st.write(complaint["description"])

            st.write("📌 Status :", complaint["status"])

            st.write("📅 Date :", complaint["created_at"])
        
# LOGOUT


with col2:
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")