# -*- coding: utf-8 -*-

import streamlit as st
from datetime import date
from database import get_connection

st.set_page_config(
    page_title="Equipment Booking",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Equipment Booking")
st.caption("Book College Lab Equipment Easily")

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")


# DELETE FUNCTION FOR EQUIPMENT BOOKINGS

def delete_equipment_booking(booking_id, user_id):
    """Delete an equipment booking only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this booking
        cursor.execute(
            "SELECT user_id FROM equipment_bookings WHERE booking_id = %s",
            (booking_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the booking
            cursor.execute(
                "DELETE FROM equipment_bookings WHERE booking_id = %s AND user_id = %s",
                (booking_id, user_id)
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
        st.error(f"Error deleting booking: {e}")
        return False


# BOOK EQUIPMENT

st.subheader("📝 Book Equipment")

equipment_name = st.text_input("Equipment Name")
category = st.selectbox(
    "Category",
    [
        "Computer Lab",
        "Electronics Lab",
        "Mechanical Lab",
        "Civil Lab",
        "Chemistry Lab",
        "Physics Lab",
        "Projector",
        "Sports Equipment",
        "Other"
    ]
)
quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=20,
    value=1
)
booking_date = st.date_input(
    "Booking Date",
    value=date.today()
)
time_slot = st.selectbox(
    "Time Slot",
    [
        "09:00 AM - 10:00 AM",
        "10:00 AM - 11:00 AM",
        "11:00 AM - 12:00 PM",
        "12:00 PM - 01:00 PM",
        "02:00 PM - 03:00 PM",
        "03:00 PM - 04:00 PM",
        "04:00 PM - 05:00 PM"
    ]
)
purpose = st.text_area(
    "Purpose",
    height=120,
    placeholder="Why do you need this equipment?"
)

st.divider()

if st.button("📅 Book Equipment", use_container_width=True):
    if equipment_name.strip()=="":
        st.error("Enter Equipment Name")
    elif purpose.strip()=="":
        st.error("Enter Purpose")
    else:
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute(
            """
            INSERT INTO equipment_bookings
            (user_id, equipment_name, category, quantity, booking_date, time_slot, purpose)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state["user_id"],
                equipment_name,
                category,
                quantity,
                booking_date,
                time_slot,
                purpose
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Equipment Booked Successfully")
        st.balloons()
        st.rerun()

st.divider()


# NAVIGATION

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()


# SEARCH BOOKINGS WITH DELETE BUTTON

st.subheader("🔍 Search Equipment")

search = st.text_input(
    "Search Equipment",
    placeholder="Search by Equipment or Category"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        e.*,
        u.full_name,
        u.user_id as owner_id
    FROM equipment_bookings e
    LEFT JOIN users u
    ON e.user_id = u.user_id
    WHERE
        e.equipment_name LIKE %s
        OR e.category LIKE %s
    ORDER BY e.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    )
)

bookings = cursor.fetchall()
cursor.close()
conn.close()

if len(bookings)==0:
    st.info("No Equipment Bookings Found")
else:
    for booking in bookings:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.subheader(booking["equipment_name"])
                st.write("🧪 Category :", booking["category"])
                st.write("📦 Quantity :", booking["quantity"])
                st.write("📅 Date :", booking["booking_date"])
                st.write("🕒 Time :", booking["time_slot"])
                
            with col2:
                st.write("👤 Student :", booking["full_name"])
                st.write("📝 Purpose :", booking["purpose"])
                
                if booking["status"]=="Pending":
                    st.warning("⏳ Pending")
                elif booking["status"]=="Approved":
                    st.success("✅ Approved")
                else:
                    st.error("❌ Rejected")

            with col3:
                
                # DELETE BUTTON - Only for post owner
                
                if st.session_state.get('user_id') == booking['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_equipment_{booking['booking_id']}",
                        use_container_width=True
                    ):
                        if delete_equipment_booking(booking['booking_id'], st.session_state['user_id']):
                            st.success("✅ Booking deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete booking")
                else:
                    st.info("🔒 Booked by other user")

st.divider()


# BOOKING SUMMARY

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM equipment_bookings")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM equipment_bookings WHERE status='Pending'")
pending = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM equipment_bookings WHERE status='Approved'")
approved = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM equipment_bookings WHERE status='Rejected'")
rejected = cursor.fetchone()[0]

cursor.close()
conn.close()

st.subheader("📊 Equipment Booking Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📦 Total", total)
with c2:
    st.metric("⏳ Pending", pending)
with c3:
    st.metric("✅ Approved", approved)
with c4:
    st.metric("❌ Rejected", rejected)

st.divider()

st.info(
"""
### 💡 Equipment Booking Guidelines

✔ Return equipment on time.
✔ Handle laboratory equipment carefully.
✔ Book only the quantity you actually need.
✔ Report damaged equipment immediately.
✔ Follow laboratory rules and faculty instructions.
✔ Equipment may require approval before use.
"""
)


# MY BOOKINGS WITH DELETE BUTTON

st.divider()
st.subheader("📋 My Bookings")

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT *
    FROM equipment_bookings
    WHERE user_id=%s
    ORDER BY created_at DESC
    """,
    (
        st.session_state["user_id"],
    )
)

my_bookings = cursor.fetchall()
cursor.close()
conn.close()

if len(my_bookings) == 0:
    st.info("You have not booked any equipment yet.")
else:
    for booking in my_bookings:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.subheader(booking["equipment_name"])
                st.write("🧪 Category :", booking["category"])
                st.write("📦 Quantity :", booking["quantity"])
                st.write("📅 Date :", booking["booking_date"])
                st.write("🕒 Time :", booking["time_slot"])
                st.write("📝 Purpose :", booking["purpose"])

                if booking["status"] == "Pending":
                    st.warning("⏳ Pending")
                elif booking["status"] == "Approved":
                    st.success("✅ Approved")
                else:
                    st.error("❌ Rejected")

            with col2:
                # Cancel button only for pending bookings
                if booking["status"] == "Pending":
                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{booking['booking_id']}",
                        use_container_width=True
                    ):
                        conn = get_connection()
                        delete_cursor = conn.cursor()
                        delete_cursor.execute(
                            "DELETE FROM equipment_bookings WHERE booking_id=%s AND user_id=%s",
                            (booking["booking_id"], st.session_state["user_id"])
                        )
                        conn.commit()
                        delete_cursor.close()
                        conn.close()
                        st.success("Booking Cancelled Successfully")
                        st.rerun()

            with col3:
        
                # DELETE BUTTON - Only for owner 
                
                if st.button(
                    "🗑️ Delete",
                    key=f"delete_my_equipment_{booking['booking_id']}",
                    use_container_width=True
                ):
                    if delete_equipment_booking(booking['booking_id'], st.session_state['user_id']):
                        st.success("✅ Booking deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete booking")

st.divider()
st.caption("🧪 CampusConnect | Equipment Booking")