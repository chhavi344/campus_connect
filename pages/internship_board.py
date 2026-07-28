# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 00:26:19 2026

@author: Lenovo
"""

import streamlit as st
from datetime import date
from database import get_connection

st.set_page_config(
    page_title="Internships",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Internship Opportunities")
st.caption("Explore and Share Internship Opportunities")

#  LOGIN CHECK

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

#  POST INTERNSHIP 

st.subheader("📢 Post Internship")

company = st.text_input("Company Name")

role = st.text_input("Role")

location = st.text_input("Location")

stipend = st.text_input("Stipend")

last_date = st.date_input(
    "Last Date",
    value=date.today()
)

apply_link = st.text_input(
    "Apply Link"
)

description = st.text_area(
    "Description"
)

if st.button(
    "Post Internship",
    use_container_width=True
):

    if company.strip() == "":
        st.error("Enter Company Name")

    elif role.strip() == "":
        st.error("Enter Role")

    elif location.strip() == "":
        st.error("Enter Location")

    elif apply_link.strip() == "":
        st.error("Enter Apply Link")

    else:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO internships
            (
                company_name,
                role,
                location,
                stipend,
                last_date,
                apply_link,
                description
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                company,
                role,
                location,
                stipend,
                last_date,
                apply_link,
                description
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        st.success("🎉 Internship Posted Successfully")

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

# ALL INTERNSHIPS


st.subheader("💼 Available Internship Opportunities")

search = st.text_input(
    "🔍 Search Internship",
    placeholder="Search by Company or Role"
)

conn = get_connection()

cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT *
    FROM internships
    WHERE
        company_name LIKE %s
        OR
        role LIKE %s
    ORDER BY created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    )
)

internships = cursor.fetchall()

if len(internships) == 0:

    if search.strip() != "":
        st.error("❌ Internship Not Found")

    else:
        st.info("No Internship Available")

else:

    for job in internships:

        with st.container(border=True):

            st.subheader(job["company_name"])

            st.write("💼 Role :", job["role"])

            st.write("📍 Location :", job["location"])

            st.write("💰 Stipend :", job["stipend"])

            st.write("📅 Last Date :", job["last_date"])

            st.write("📝 Description :")

            st.write(job["description"])

            st.link_button(
                "🔗 Apply Now",
                job["apply_link"]
            )

cursor.close()
conn.close()

# LOGOUT
with col2:
    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")