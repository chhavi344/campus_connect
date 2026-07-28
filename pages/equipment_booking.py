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


# BOOK EQUIPMENT

st.subheader("📝 Book Equipment")

equipment_name = st.text_input(
    "Equipment Name"
)

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

if st.button(
    "📅 Book Equipment",
    use_container_width=True
):

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
            (
                user_id,
                equipment_name,
                category,
                quantity,
                booking_date,
                time_slot,
                purpose
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s
            )
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


# SEARCH BOOKINGS

st.divider()

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
        u.full_name
    FROM equipment_bookings e
    LEFT JOIN users u
    ON e.user_id=u.user_id
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

if len(bookings)==0:

    st.info("No Equipment Bookings Found")

else:

    for booking in bookings:

        with st.container(border=True):

            st.subheader(
                booking["equipment_name"]
            )

            c1,c2 = st.columns(2)

            with c1:

                st.write("👤 Student :", booking["full_name"])

                st.write("🧪 Category :", booking["category"])

                st.write("📦 Quantity :", booking["quantity"])

                st.write("📅 Date :", booking["booking_date"])

            with c2:

                st.write("🕒 Time :", booking["time_slot"])

                st.write("📝 Purpose :", booking["purpose"])

                if booking["status"]=="Pending":

                    st.warning("⏳ Pending")

                elif booking["status"]=="Approved":

                    st.success("✅ Approved")

                else:

                    st.error("❌ Rejected")

st.divider()

cursor.close()

conn.close()

# BOOKING SUMMARY

st.divider()

conn = get_connection()

cursor = conn.cursor()

# Total Bookings
cursor.execute(
    """
    SELECT COUNT(*)
    FROM equipment_bookings
    """
)

total = cursor.fetchone()[0]

# Pending
cursor.execute(
    """
    SELECT COUNT(*)
    FROM equipment_bookings
    WHERE status='Pending'
    """
)

pending = cursor.fetchone()[0]

# Approved
cursor.execute(
    """
    SELECT COUNT(*)
    FROM equipment_bookings
    WHERE status='Approved'
    """
)

approved = cursor.fetchone()[0]

# Rejected
cursor.execute(
    """
    SELECT COUNT(*)
    FROM equipment_bookings
    WHERE status='Rejected'
    """
)

rejected = cursor.fetchone()[0]

cursor.close()
conn.close()

st.subheader("📊 Equipment Booking Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Total",
        total
    )

with c2:
    st.metric(
        "⏳ Pending",
        pending
    )

with c3:
    st.metric(
        "✅ Approved",
        approved
    )

with c4:
    st.metric(
        "❌ Rejected",
        rejected
    )

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

# MY BOOKINGS


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

if len(my_bookings) == 0:

    st.info("You have not booked any equipment yet.")

else:

    for booking in my_bookings:

        with st.container(border=True):

            c1, c2 = st.columns([4,1])

            with c1:

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

            with c2:

                if booking["status"] == "Pending":

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{booking['booking_id']}",
                        use_container_width=True
                    ):

                        delete_cursor = conn.cursor()

                        delete_cursor.execute(
                            """
                            DELETE FROM equipment_bookings
                            WHERE booking_id=%s
                            """,
                            (
                                booking["booking_id"],
                            )
                        )

                        conn.commit()

                        delete_cursor.close()

                        st.success("Booking Cancelled Successfully")

                        st.rerun()

cursor.close()
conn.close()

