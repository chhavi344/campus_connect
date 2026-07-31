
import streamlit as st
import os
from datetime import datetime
from database import get_connection

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)

# Check Login
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# Create upload folder
UPLOAD_FOLDER = "uploads/profile_pictures"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# CUSTOM CSS - EXACT DASHBOARD THEME

st.markdown("""
<style>
    /* 1. App Background */
    .stApp {
        background-color: #f8f6fc !important;
    }

    /* 2. STREAMLIT SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    section[data-testid="stSidebar"] .st-emotion-cache-1v0mbdj {
        background-color: #eae4f5 !important;
        color: #4a154b !important;
        border-radius: 8px !important;
    }

    /* 3. Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 4. Main Profile Container */
    .profile-container {
        background: #ffffff;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f0ebf8;
    }

    /* 5. Profile Avatar - EXACT FIX */
    .avatar-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .avatar-image {
        width: 160px !important;
        height: 160px !important;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #eae4f5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* 6. Typography */
    .profile-name { font-size: 32px; font-weight: 600; color: #1a1a1a; margin: 0px 0 5px 0; }
    .profile-text { color: #555555; font-size: 15px; margin: 5px 0; }
    .profile-icon { color: #6c5ce7; margin-right: 8px; }

    /* 7. Stats Container */
    .stats-container {
        display: flex; justify-content: space-between;
        background: #faf8fd; padding: 20px 15px;
        border-radius: 12px; margin-top: 20px;
        border: 1px solid #f0ebf8;
    }
    .stat-item { text-align: center; flex: 1; }
    .stat-number { font-size: 24px; font-weight: 700; color: #4a154b; display: block; }
    .stat-label { font-size: 12px; color: #888888; text-transform: uppercase; margin-top: 4px; }

    /* 8. Buttons */
    .stButton > button {
        background: #f8f6fc !important; color: #4a154b !important;
        border: 1px solid #eae4f5 !important; border-radius: 8px !important;
        padding: 10px 0px !important; font-size: 15px !important;
        transition: 0.3s ease !important; width: 100%;
    }
    .stButton > button:hover {
        background: #eae4f5 !important; border-color: #6c5ce7 !important;
    }

    /* 9. Activity Cards */
    .activity-card {
        background: #ffffff; border-radius: 12px; padding: 20px 10px;
        text-align: center; border: 1px solid #f0ebf8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); transition: 0.3s ease;
    }
    .activity-card:hover { transform: translateY(-3px); border-color: #eae4f5; }
    .activity-number { font-size: 24px; font-weight: 700; color: #4a154b; }
    .activity-label { font-size: 13px; color: #666666; margin-top: 5px; }
    
    /* Fix padding */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
</style>
""", unsafe_allow_html=True)

# FUNCTION TO UPDATE PROFILE PICTURE

def update_profile_picture(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1]
            filename = f"user_{st.session_state['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET profile_image=%s WHERE user_id=%s",
                (filepath, st.session_state['user_id'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            # Update session state so it shows immediately on next load
            st.session_state.profile_image = filepath
            return True, "✅ Profile Picture Updated Successfully!"
    except Exception as e:
        return False, f"Error: {e}"
    return False, "No file selected"


# GET USER DATA

def get_user_data(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        return None

user_data = get_user_data(st.session_state['user_id'])

if user_data:
    
    # PROFILE HEADER
    
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2.2])
    
    with col1:
        profile_img = user_data.get('profile_image')
        
        
        st.markdown('<div class="avatar-wrapper">', unsafe_allow_html=True)
        if profile_img and os.path.exists(profile_img):
            st.image(profile_img, width=160, output_format="JPEG")
        else:
            
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=160)
        st.markdown('</div>', unsafe_allow_html=True)
        
    
        uploaded_file = st.file_uploader(
            "📸 Change Photo",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="profile_uploader"
        )
        
        if uploaded_file is not None:
            col_up, col_can = st.columns(2)
            with col_up:
                if st.button("✅ Upload", use_container_width=True):
                    success, message = update_profile_picture(uploaded_file)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun() # Forces page to reload and show new image
                    else:
                        st.error(message)
            with col_can:
                if st.button("❌ Cancel", use_container_width=True):
                    st.rerun()
        
        if user_data.get('profile_image') and os.path.exists(user_data.get('profile_image', '')):
            if st.button("🗑️ Remove", use_container_width=True):
                try:
                    if os.path.exists(user_data['profile_image']):
                        os.remove(user_data['profile_image'])
                    
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET profile_image=NULL WHERE user_id=%s",
                        (st.session_state['user_id'],)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    st.session_state.profile_image = None
                    st.success("✅ Removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        # Name and Bio
        st.markdown(f'<div class="profile-name">{user_data["full_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="profile-text"><span class="profile-icon">📧</span> {user_data["email"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="profile-text"><span class="profile-icon">🏫</span> {user_data.get("department", "Not Provided")} • <span class="profile-icon">📚</span> {user_data.get("semester", "Not Provided")}</div>', unsafe_allow_html=True)
        
        # Stats
        try:
            conn = get_connection()
            cursor = conn.cursor()
            user_id = st.session_state['user_id']
            
            cursor.execute("SELECT COUNT(*) FROM lost_items WHERE user_id=%s", (user_id,))
            lost = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM books WHERE user_id=%s", (user_id,))
            books = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id=%s", (user_id,))
            notes = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM rides WHERE user_id=%s", (user_id,))
            rides = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM events WHERE user_id=%s", (user_id,))
            events = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM complaints WHERE user_id=%s", (user_id,))
            complaints = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            st.markdown(f"""
            <div class="stats-container">
                <div class="stat-item">
                    <span class="stat-number">{lost}</span>
                    <span class="stat-label">Lost</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{books + notes}</span>
                    <span class="stat-label">Books & Notes</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{rides + events}</span>
                    <span class="stat-label">Rides & Events</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{complaints}</span>
                    <span class="stat-label">Complaints</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            pass
        
        # Edit Profile Button
        with st.expander("✏️ Edit Profile", expanded=False):
            with st.form("update_profile_form"):
                full_name = st.text_input("Full Name", value=user_data['full_name'])
                phone = st.text_input("Phone Number", value=user_data.get('phone') or '')
                department = st.text_input("Department", value=user_data.get('department') or '')
                semester_options = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"]
                current_semester = user_data.get('semester') or "Semester 1"
                semester_index = semester_options.index(current_semester) if current_semester in semester_options else 0
                semester = st.selectbox("Semester", semester_options, index=semester_index)
                
                if st.form_submit_button("💾 Update Profile", use_container_width=True):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            """UPDATE users SET full_name=%s, phone=%s, department=%s, semester=%s WHERE user_id=%s""",
                            (full_name, phone, department, semester, st.session_state['user_id'])
                        )
                        conn.commit()
                        st.session_state.full_name = full_name
                        st.session_state.phone = phone
                        st.session_state.department = department
                        st.session_state.semester = semester
                        cursor.close()
                        conn.close()
                        st.success("✅ Profile Updated!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    

    # ACTIVITY STATS
    
    st.markdown('<h4 style="color: #333333; margin: 15px 0 15px 0;">📊 My Activity</h4>', unsafe_allow_html=True)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        user_id = st.session_state['user_id']
        cursor.execute("SELECT COUNT(*) FROM lost_items WHERE user_id=%s", (user_id,))
        lost = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM found_items WHERE user_id=%s", (user_id,))
        found = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM books WHERE user_id=%s", (user_id,))
        books = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id=%s", (user_id,))
        notes = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="activity-card"><div class="activity-number">{lost}</div><div class="activity-label">📍 Lost</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="activity-card"><div class="activity-number">{found}</div><div class="activity-label">🔍 Found</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="activity-card"><div class="activity-number">{books}</div><div class="activity-label">📚 Books</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="activity-card"><div class="activity-number">{notes}</div><div class="activity-label">📝 Notes</div></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

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

    st.markdown('<p style="text-align: center; color: #999999; font-size: 12px; margin-top: 10px;">🎓 CampusConnect | My Profile</p>', unsafe_allow_html=True)