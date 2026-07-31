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


# DELETE FUNCTION

def delete_event(event_id, user_id):
    """Delete an event only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this event
        cursor.execute(
            "SELECT user_id FROM events WHERE event_id = %s",
            (event_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the event
            cursor.execute(
                "DELETE FROM events WHERE event_id = %s AND user_id = %s",
                (event_id, user_id)
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
        st.error(f"Error deleting event: {e}")
        return False

 
# CREATE UPLOAD FOLDER

UPLOAD_FOLDER = "uploads/event_posters"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# POST NEW EVENT

st.subheader("📢 Post New Event")

event_name = st.text_input("Event Name")
description = st.text_area("Event Description")
event_date = st.date_input("Event Date", value=date.today())
event_time = st.time_input("Event Time")
venue = st.text_input("Venue")
poster = st.file_uploader(
    "Upload Event Poster",
    type=["jpg", "jpeg", "png"]
)

if st.button("Post Event", use_container_width=True):

    if event_name.strip() == "":
        st.error("Enter Event Name")
    elif description.strip() == "":
        st.error("Enter Description")
    elif venue.strip() == "":
        st.error("Enter Venue")
    else:
        poster_path = ""
        if poster is not None:
            poster_path = os.path.join(UPLOAD_FOLDER, poster.name)
            with open(poster_path, "wb") as f:
                f.write(poster.getbuffer())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events
            (user_id, event_name, description, event_date, event_time, venue, poster_path)
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

st.divider()


# NAVIGATION BUTTONS

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.divider()


# ALL EVENTS WITH DELETE BUTTON

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
        u.full_name,
        u.user_id as owner_id
    FROM events e
    LEFT JOIN users u
    ON e.user_id = u.user_id
    WHERE
        e.event_name LIKE %s
    ORDER BY e.event_date ASC
    """,
    (
        "%" + search + "%",
    )
)

events = cursor.fetchall()
cursor.close()
conn.close()

if len(events) == 0:
    if search.strip() != "":
        st.error("❌ No Event Found")
    else:
        st.info("No Events Available")
else:
    for event in events:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if event["poster_path"]:
                    if os.path.exists(event["poster_path"]):
                        st.image(event["poster_path"], width=180)

            with col2:
                st.subheader(event["event_name"])
                st.write("📅 Date :", event["event_date"])
                st.write("⏰ Time :", event["event_time"])
                st.write("📍 Venue :", event["venue"])
                st.write("📝 Description :")
                st.write(event["description"])
                
                # Show who posted
                st.caption(f"👤 Posted By: {event['full_name']}")

            with col3:
                
                # DELETE BUTTON - Only for post owner
                
                if st.session_state.get('user_id') == event['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_event_{event['event_id']}",
                        use_container_width=True
                    ):
                        if delete_event(event['event_id'], st.session_state['user_id']):
                            st.success("✅ Event deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete event")
                else:
                    st.info("🔒 Post by other user")

st.divider()


# LOGOUT

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()
st.caption("🎉 CampusConnect | Club Events")