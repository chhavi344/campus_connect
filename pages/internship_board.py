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

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# DELETE FUNCTION

def delete_internship(internship_id, user_id):
    """Delete an internship only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this internship
        cursor.execute(
            "SELECT user_id FROM internships WHERE internship_id = %s",
            (internship_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the internship
            cursor.execute(
                "DELETE FROM internships WHERE internship_id = %s AND user_id = %s",
                (internship_id, user_id)
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
        st.error(f"Error deleting internship: {e}")
        return False

# 
# POST INTERNSHIP
# 
st.subheader("📢 Post Internship")

company = st.text_input("Company Name")
role = st.text_input("Role")
location = st.text_input("Location")
stipend = st.text_input("Stipend")
last_date = st.date_input("Last Date", value=date.today())
apply_link = st.text_input("Apply Link")
description = st.text_area("Description")

if st.button("Post Internship", use_container_width=True):
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
            (user_id, company_name, role, location, stipend, last_date, apply_link, description)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state.get("user_id"),
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

st.divider()


# NAVIGATION BUTTONS

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.divider()


# ALL INTERNSHIPS WITH DELETE BUTTON

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
cursor.close()
conn.close()

if len(internships) == 0:
    if search.strip() != "":
        st.error("❌ Internship Not Found")
    else:
        st.info("No Internship Available")
else:
    for job in internships:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
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

            with col2:
                
                # DELETE BUTTON 
                if st.session_state.get('user_id') == job.get('user_id'):
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_internship_{job['internship_id']}",
                        use_container_width=True
                    ):
                        if delete_internship(job['internship_id'], st.session_state['user_id']):
                            st.success("✅ Internship deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete internship")
                else:
                    st.info("🔒 Posted by other user")

st.divider()


with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()
st.caption("💼 CampusConnect | Internship Board")