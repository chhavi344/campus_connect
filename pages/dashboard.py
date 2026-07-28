import streamlit as st
from datetime import datetime

#PAGE SETTINGS

st.set_page_config(
    page_title="CampusConnect Dashboard",
    page_icon="🎓",
    layout="wide"
)

# LOGIN CHECK

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

#  HEADER

st.title("🎓 CampusConnect Dashboard")

name = st.session_state.get("full_name", "Student")
email = st.session_state.get("email", "")

st.success(f"👋 Welcome, {name}")

today = datetime.now()

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"📧 {email}")

with col2:
    st.info(f"📅 {today.strftime('%d %B %Y')}")

with col3:
    st.info(f"🕒 {today.strftime('%I:%M %p')}")

st.divider()

# SEARCH 

search = st.text_input(
    "🔍 Search CampusConnect",
    placeholder="Search books, notes, events, internships, lost items..."
)

st.divider()

# QUICK ACTIONS 

st.subheader("⚡ Quick Actions")

q1, q2, q3, q4 = st.columns(4)

with q1:

    if st.button(
        "📍 Report Lost Item",
        use_container_width=True
    ):
        st.switch_page("pages/lost_found.py")

with q2:

    if st.button(
        "📚 Upload Notes",
        use_container_width=True
    ):
        st.switch_page("pages/notes_sharing.py")

with q3:

    if st.button(
        "📖 Sell Book",
        use_container_width=True
    ):
        st.switch_page("pages/book_exchange.py")

with q4:

    if st.button(
        "🎉 Create Event",
        use_container_width=True
    ):
        st.switch_page("pages/club_events.py")

st.write("")

q5, q6, q7, q8 = st.columns(4)

with q5:

    st.button(
    "🚗 Offer Ride",
    key="quick_offer_ride",
    use_container_width=True
)
    

with q6:

  st.button(
    "🛠 Raise Complaint",
    key="quick_raise_complaint",
    use_container_width=True
)

with q7:

   st.button(
    "👤 My Profile",
    key="quick_profile",
    use_container_width=True
)

with q8:

   st.button(
    "🔔 Notifications",
    key="quick_notifications",
    use_container_width=True
)

st.divider()

# CAMPUS MODULES

st.subheader("📦 Campus Modules")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "📍 Lost & Found",
        use_container_width=True
    ):
        st.switch_page("pages/lost_found.py")

    if st.button(
        "📝 Notes Sharing",
        use_container_width=True
    ):
        st.switch_page("pages/notes_sharing.py")

    if st.button(
        "🚗 Ride Sharing",
        key="module_ride_sharing",
        use_container_width=True
    ):
        st.switch_page("pages/ride_sharing.py")

    if st.button(
        "🧪 Equipment Booking",
        key="module_equipment",
        use_container_width=True,
    ):
        st.switch_page("pages/equipment_booking.py")

with c2:

    if st.button(
        "📚 Book Exchange",
        use_container_width=True
    ):
        st.switch_page("pages/book_exchange.py")

    if st.button(
        "💼 Internship Board",
        key="module_internship",
        use_container_width=True
    ):
        st.switch_page("pages/internship_board.py")

    if st.button(
        "🏠 Hostel Marketplace",
        key="module_hostel_market",
        use_container_width=True
    ):
        st.switch_page("pages/hostel_marketplace.py")

    st.button(
        "🔔 Notifications",
        key="module_notifications",
        use_container_width=True
    )

with c3:

    if st.button(
        "🎉 Club Events",
        use_container_width=True
    ):
        st.switch_page("pages/club_events.py")

    if st.button(
        "👨‍🏫 Mentor Connect",
        key="module_mentor",
        use_container_width=True
    ):
        st.switch_page("pages/mentor_matching.py")

    if st.button(
        "🛠 Complaint Portal",
        key="module_complaint",
        use_container_width=True
    ):
        st.switch_page("pages/complaint_portal.py")

    if st.button(
        "⚙ Settings",
        key="module_settings",
        use_container_width=True
    ):
        pass
# QUICK STATS

st.subheader("📊 Campus Statistics")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(
        label="📍 Lost Items",
        value="24"
    )

with s2:
    st.metric(
        label="📚 Books Available",
        value="18"
    )

with s3:
    st.metric(
        label="📝 Notes Uploaded",
        value="67"
    )

with s4:
    st.metric(
        label="🎉 Upcoming Events",
        value="9"
    )

st.divider()

# RECENT UPDATES 

st.subheader("📢 Recent Updates")

left, right = st.columns(2)

with left:

    st.info("📍 Wallet Found near Central Library")

    st.info("📚 Operating System Notes Uploaded")

    st.info("📖 Data Structures Book Available")

    st.info("🚗 Ride Available to Railway Station")

with right:

    st.info("🎉 Coding Club Registration Open")

    st.info("💼 TCS Internship Applications Started")

    st.info("🛠 Complaint Resolved Successfully")

    st.info("👨‍🏫 New Mentor Added")

st.divider()

# UPCOMING EVENTS 

st.subheader("🎉 Upcoming Events")

e1, e2 = st.columns(2)

with e1:

    st.success("💻 Hackathon 2026")
    st.write("📅 20 July 2026")
    st.write("📍 Seminar Hall")

    st.button(
        "Register",
        key="hackathon",
        use_container_width=True
    )

with e2:

    st.success("🤖 AI Workshop")
    st.write("📅 25 July 2026")
    st.write("📍 Lab 4")

    st.button(
        "Register",
        key="ai",
        use_container_width=True
    )

st.divider()

# FEATURED BOOKS 

st.subheader("📚 Recently Added Books")

b1, b2, b3 = st.columns(3)

with b1:

    st.success("Database Management System")

    st.write("Semester 4")

    st.button(
        "View",
        key="book1",
        use_container_width=True
    )

with b2:

    st.success("Operating System")

    st.write("Semester 5")

    st.button(
        "View",
        key="book2",
        use_container_width=True
    )

with b3:

    st.success("Computer Networks")

    st.write("Semester 6")

    st.button(
        "View",
        key="book3",
        use_container_width=True
    )

st.divider() 
# MY PROFILE

st.subheader("👤 My Profile")

col1, col2 = st.columns([1,3])

with col1:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

with col2:

    st.write(f"**👤 Name :** {st.session_state.get('full_name','Student')}")

    st.write(f"**📧 Email :** {st.session_state.get('email','Not Available')}")

    st.write("**🏫 Department :** CSE")

    st.write("**📚 Semester :** Semester 6")

st.divider()

# MY ACTIVITY 

st.subheader("📋 My Activity")

a1, a2, a3 = st.columns(3)

with a1:

    st.success("📍 Lost Items")
    st.metric(
        "Reports",
        "2"
    )

with a2:

    st.success("📚 Notes Uploaded")
    st.metric(
        "Uploads",
        "5"
    )

with a3:

    st.success("📖 Books Listed")
    st.metric(
        "Books",
        "3"
    )

st.divider()

# ANNOUNCEMENTS 

st.subheader("📢 Announcements")

st.warning("📅 Semester Examination Form is Live.")

st.warning("🎉 Independence Day Celebration Registration Open.")

st.warning("💼 New Internship Opportunities Available.")

st.divider()

# HELP 

with st.expander("ℹ Need Help?"):

    st.markdown("""
### CampusConnect Guide

- 📍 Report Lost & Found Items
- 📚 Exchange Books
- 📝 Share Notes
- 🎉 Join Club Events
- 🚗 Share Rides
- 💼 Apply for Internships
- 👨‍🏫 Connect with Mentors
- 🛠 Raise Complaints

Your data is securely stored in the CampusConnect database.
""")

st.divider()

# footer

left, right = st.columns(2)

#with left:

 #   if st.button(
  #      "🏠 Home",
   #     use_container_width=True
   # ):

    #    st.rerun()

with right:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.success("Logged Out Successfully")

        st.switch_page("app.py")

st.divider()

st.caption("🎓 CampusConnect | Smart Campus Management System")