import streamlit as st

st.set_page_config(
    page_title="CampusConnect",
    page_icon="🎓",
    layout="wide"
)

# TITLE 
st.title("🎓 CampusConnect")

st.subheader("Your Smart Campus Companion")

st.write(
    "CampusConnect is a one-stop platform where students can access all campus services easily."
)

st.divider()

# FEATURES 

st.subheader("✨ Features")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("📍 Lost & Found")

with c2:
    st.info("📚 Book Exchange")

with c3:
    st.info("📄 Notes Sharing")

with c4:
    st.info("🎉 Club Events")

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.info("🚗 Ride Sharing")

with c6:
    st.info("👨‍🏫 Mentor Matching")

with c7:
    st.info("💼 Internship Board")

with c8:
    st.info("📝 Complaint Portal")

st.divider()

# BUTTONS 

st.subheader("Get Started")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")

with col2:
    if st.button("📝 Sign Up", use_container_width=True):
        st.switch_page("pages/signup.py")

st.divider()

# ABOUT 
st.subheader("About CampusConnect")

st.write("""
CampusConnect helps students:

- 📍 Report Lost & Found items
- 📚 Exchange books
- 📄 Upload and download notes
- 🎉 Join club events
- 🚗 Share rides
- 👨‍🏫 Connect with mentors
- 💼 Find internships
- 📝 Raise campus complaints
""")

st.divider()

st.caption("© 2026 CampusConnect | Developed using Streamlit & MySQL")