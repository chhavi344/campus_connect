import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Mentor Connect",
    page_icon="👨‍🏫",
    layout="wide"
)

st.title("👨‍🏫 Mentor Connect")
st.caption("Connect with Student Mentors")

#  LOGIN CHECK 

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# ADD MENTOR 

st.subheader("➕ Add Mentor")

mentor_name = st.text_input("Mentor Name")

department = st.text_input("Department")

skills = st.text_area("Skills")

availability = st.selectbox(
    "Availability",
    [
        "Morning",
        "Afternoon",
        "Evening",
        "Weekend"
    ]
)

contact = st.text_input("Contact Number")

if st.button(
    "Add Mentor",
    use_container_width=True
):

    if mentor_name.strip() == "":
        st.error("Enter Mentor Name")

    elif department.strip() == "":
        st.error("Enter Department")

    elif skills.strip() == "":
        st.error("Enter Skills")

    elif contact.strip() == "":
        st.error("Enter Contact Number")

    else:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO mentors
            (
                user_id,
                mentor_name,
                department,
                skills,
                availability,
                contact
            )
            VALUES(%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state["user_id"],
                mentor_name,
                department,
                skills,
                availability,
                contact
            )
        )

        conn.commit()

        cursor.close()

        conn.close()

        st.success("✅ Mentor Added Successfully")

        st.balloons()

        st.rerun()
        
# DASHBOARD & LOGOUT


st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()


# SEARCH MENTORS


st.subheader("👨‍🏫 Available Mentors")

search = st.text_input(
    "🔍 Search Mentor",
    placeholder="Search by Mentor Name, Department or Skills"
)

conn = get_connection()

cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        m.*,
        u.full_name
    FROM mentors m
    LEFT JOIN users u
    ON m.user_id = u.user_id
    WHERE
        m.mentor_name LIKE %s
        OR m.department LIKE %s
        OR m.skills LIKE %s
    ORDER BY m.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
    )
)

mentors = cursor.fetchall()

if len(mentors) == 0:

    if search.strip() != "":
        st.error("❌ Mentor Not Found")

    else:
        st.info("No Mentors Available")

else:

    for mentor in mentors:

        with st.container(border=True):

            st.subheader(mentor["mentor_name"])

            st.write("👤 Added By :", mentor["full_name"])
            st.write("🏫 Department :", mentor["department"])
            st.write("💡 Skills :", mentor["skills"])
            st.write("🕒 Availability :", mentor["availability"])
            st.write("📞 Contact :", mentor["contact"])
            st.write("📅 Added On :", mentor["created_at"])

cursor.close()
conn.close()