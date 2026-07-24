import streamlit as st
import os
from datetime import date
from database import get_connection

st.set_page_config(
    page_title="Club Events",
    page_icon="🎉",
    layout="wide"
)

st.title("🎉 Club Events")
st.caption("Post and Explore Campus Events")

# login

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# create folder

UPLOAD_FOLDER = "uploads/event_posters"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# event form 

st.subheader("📢 Post New Event")

event_name = st.text_input(
    "Event Name"
)

description = st.text_area(
    "Event Description"
)

event_date = st.date_input(
    "Event Date",
    value=date.today()
)

event_time = st.time_input(
    "Event Time"
)

venue = st.text_input(
    "Venue"
)

poster = st.file_uploader(
    "Upload Event Poster",
    type=["jpg", "jpeg", "png"]
)

if st.button(
    "Post Event",
    use_container_width=True
):

    if event_name.strip() == "":
        st.error("Enter Event Name")

    elif description.strip() == "":
        st.error("Enter Description")

    elif venue.strip() == "":
        st.error("Enter Venue")

    else:

        poster_path = ""

        if poster is not None:

            poster_path = os.path.join(
                UPLOAD_FOLDER,
                poster.name
            )

            with open(poster_path, "wb") as f:
                f.write(poster.getbuffer())

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO events
            (
                user_id,
                event_name,
                description,
                event_date,
                event_time,
                venue,
                poster_path
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state.get("user_id"),
                event_name,
                description,
                event_date,
                event_time,
                venue,
                poster_path
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        st.success("🎉 Event Posted Successfully")

        st.balloons()

        st.rerun()
    
# dashboard button 

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.divider()

# all events

st.subheader("📅 All Club Events")

search = st.text_input(
    "🔍 Search Events",
    placeholder="Search by Event Name"
)

conn = get_connection()

cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        e.*,
        u.full_name
    FROM events e
    LEFT JOIN users u
    ON e.user_id=u.user_id
    WHERE
        e.event_name LIKE %s
    ORDER BY e.event_date ASC
    """,
    (
        "%" + search + "%",
    )
)

events = cursor.fetchall()

if len(events) == 0:

    if search.strip() != "":
        st.error("❌ No Event Found")
    else:
        st.info("No Events Available")

else:

    for event in events:

        with st.container(border=True):

            col1, col2 = st.columns([1,3])

            with col1:

                if event["poster_path"]:

                    if os.path.exists(event["poster_path"]):
                        st.image(
                            event["poster_path"],
                            width=200
                        )

            with col2:

                st.subheader(event["event_name"])

                st.write("👤 Posted By :", event["full_name"])

                st.write("📅 Date :", event["event_date"])

                st.write("⏰ Time :", event["event_time"])

                st.write("📍 Venue :", event["venue"])

                st.write("📝 Description :")

                st.write(event["description"])

cursor.close()
conn.close()
# login button 

with col2:
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")