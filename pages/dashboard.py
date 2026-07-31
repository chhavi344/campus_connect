# dashboard.py
import streamlit as st
from datetime import datetime
from database import get_connection

# PAGE SETTINGS
st.set_page_config(
    page_title="CampusConnect Dashboard",
    page_icon="🎓",
    layout="wide"
)

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")


# FETCH STATISTICS

def get_stats():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM lost_items WHERE status != 'Found'")
        stats['lost_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM books WHERE status='Available'")
        stats['books_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM notes")
        stats['notes_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM events WHERE event_date >= CURDATE()")
        stats['events_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM rides WHERE status='Available'")
        stats['rides_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status='Pending'")
        stats['complaints_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM marketplace WHERE status='Available'")
        stats['marketplace_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM internships WHERE last_date >= CURDATE()")
        stats['internship_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM mentors")
        stats['mentor_count'] = cursor.fetchone()['count'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM equipment_bookings WHERE status='Pending'")
        stats['equipment_count'] = cursor.fetchone()['count'] or 0
        
        cursor.close()
        conn.close()
        
        return stats
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


# YOUR ORIGINAL THEME CSS 
st.markdown("""
<style>
/* Main Container */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 10px;
}

/* Header */
.welcome-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    padding: 25px 30px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    color: white;
}
.welcome-text {
    font-size: 24px;
    font-weight: 600;
}
.welcome-subtext {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 4px;
}
.welcome-email {
    font-size: 13px;
    opacity: 0.8;
}
.welcome-date {
    text-align: right;
    font-size: 14px;
    opacity: 0.9;
}

/* Module Cards */
.module-card {
    background: white;
    border-radius: 14px;
    padding: 20px 15px;
    text-align: center;
    border: 1px solid #e8ecf1;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    height: 100%;
}
.module-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border-color: #667eea;
}
.module-icon {
    font-size: 30px;
    margin-bottom: 8px;
}
.module-name {
    font-weight: 600;
    color: #1a1a2e;
    font-size: 14px;
    margin: 5px 0;
}
.module-desc {
    font-size: 11px;
    color: #8e8e8e;
    margin: 3px 0 10px 0;
}

/* Stat Cards - Your Colors */
.stat-card {
    border-radius: 12px;
    padding: 14px 10px;
    text-align: center;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    cursor: pointer;
    border: none;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.stat-icon {
    font-size: 20px;
}
.stat-number {
    font-size: 24px;
    font-weight: 700;
    margin: 2px 0;
}
.stat-label {
    font-size: 10px;
    opacity: 0.9;
    font-weight: 500;
}

/* Stat Colors - Aesthetic */
.stat-rose { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-sunset { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
.stat-ocean { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-forest { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.stat-lavender { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
.stat-peach { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); }
.stat-mint { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); color: #1a1a2e; }
.stat-coral { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.stat-sky { background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%); }
.stat-blush { background: linear-gradient(135deg, #fccb90 0%, #d57eeb 100%); }

/* Section Title */
.section-title {
    color: #1a1a2e;
    font-size: 20px;
    font-weight: 600;
    margin: 20px 0 15px 0;
}
.section-title span {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 11px;
    color: white;
    margin-left: 8px;
}

/* Divider */
.custom-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #e8ecf1, transparent);
    margin: 25px 0;
}

/* Footer */
.footer-text {
    color: #8e8e8e;
    font-size: 13px;
    text-align: center;
    padding: 15px 0;
}

/* Button Styles */
.stButton button {
    border-radius: 8px;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Info Boxes */
.stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 10px !important;
}

/* Full width container */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)


# HEADER - Your Style

st.markdown(f"""
<div class="welcome-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 28px;">🎓</span>
                <span style="font-size: 22px; font-weight: 700;">CampusConnect</span>
            </div>
            <div class="welcome-text">Welcome back, {st.session_state.get('full_name', 'Student')}! 👋</div>
            <div class="welcome-email">📧 {st.session_state.get('email', '')}</div>
        </div>
        <div class="welcome-date">
            <div>📅 {datetime.now().strftime('%d %B %Y')}</div>
            <div>🕒 {datetime.now().strftime('%I:%M %p')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# CAMPUS MODULES

st.markdown('<div class="section-title">📦 Campus Modules <span>12</span></div>', unsafe_allow_html=True)

modules = [
    {"name": "Lost & Found", "icon": "📍", "page": "pages/lost_found.py", "desc": "Report lost/found items"},
    {"name": "Book Exchange", "icon": "📚", "page": "pages/book_exchange.py", "desc": "Exchange books"},
    {"name": "Club Events", "icon": "🎉", "page": "pages/club_events.py", "desc": "Create/join events"},
    {"name": "Notes Sharing", "icon": "📝", "page": "pages/notes_sharing.py", "desc": "Share study notes"},
    {"name": "Internship Board", "icon": "💼", "page": "pages/internship_board.py", "desc": "Find internships"},
    {"name": "Mentor Connect", "icon": "👨‍🏫", "page": "pages/mentor_matching.py", "desc": "Find mentors"},
    {"name": "Ride Sharing", "icon": "🚗", "page": "pages/ride_sharing.py", "desc": "Share rides"},
    {"name": "Hostel Marketplace", "icon": "🏠", "page": "pages/hostel_marketplace.py", "desc": "Buy/sell items"},
    {"name": "Complaint Portal", "icon": "🛠", "page": "pages/complaint_portal.py", "desc": "Raise complaints"},
    {"name": "Equipment Booking", "icon": "🧪", "page": "pages/equipment_booking.py", "desc": "Book equipment"},
    {"name": "Notifications", "icon": "🔔", "page": "pages/notifications.py", "desc": "View notifications"},
    {"name": "My Profile", "icon": "👤", "page": "pages/profile.py", "desc": "Manage profile"},
]

# Display modules in 4-column grid
cols = st.columns(4)

for idx, module in enumerate(modules):
    col_idx = idx % 4
    with cols[col_idx]:
        st.markdown(f"""
        <div class="module-card">
            <div class="module-icon">{module['icon']}</div>
            <div class="module-name">{module['name']}</div>
            <div class="module-desc">{module['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "Open →",
            key=f"module_{idx}",
            use_container_width=True
        ):
            st.switch_page(module['page'])

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# CAMPUS STATISTICS

stats = get_stats()

if stats:
    st.markdown('<div class="section-title">📊 Campus Statistics <span>Live</span></div>', unsafe_allow_html=True)
    
    # Row 1 - 5 columns
    s1, s2, s3, s4, s5 = st.columns(5)
    
    with s1:
        st.markdown(f"""
        <div class="stat-card stat-rose">
            <div class="stat-icon">📍</div>
            <div class="stat-number">{stats['lost_count']}</div>
            <div class="stat-label">Lost Items</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📍", key="stat_lost", use_container_width=True):
            st.switch_page("pages/lost_found.py")
    
    with s2:
        st.markdown(f"""
        <div class="stat-card stat-forest">
            <div class="stat-icon">📚</div>
            <div class="stat-number">{stats['books_count']}</div>
            <div class="stat-label">Books</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📚", key="stat_books", use_container_width=True):
            st.switch_page("pages/book_exchange.py")
    
    with s3:
        st.markdown(f"""
        <div class="stat-card stat-ocean">
            <div class="stat-icon">📝</div>
            <div class="stat-number">{stats['notes_count']}</div>
            <div class="stat-label">Notes</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝", key="stat_notes", use_container_width=True):
            st.switch_page("pages/notes_sharing.py")
    
    with s4:
        st.markdown(f"""
        <div class="stat-card stat-sunset">
            <div class="stat-icon">🎉</div>
            <div class="stat-number">{stats['events_count']}</div>
            <div class="stat-label">Events</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎉", key="stat_events", use_container_width=True):
            st.switch_page("pages/club_events.py")
    
    with s5:
        st.markdown(f"""
        <div class="stat-card stat-lavender">
            <div class="stat-icon">🚗</div>
            <div class="stat-number">{stats['rides_count']}</div>
            <div class="stat-label">Rides</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚗", key="stat_rides", use_container_width=True):
            st.switch_page("pages/ride_sharing.py")
    
    # Row 2 - 5 columns
    s6, s7, s8, s9, s10 = st.columns(5)
    
    with s6:
        st.markdown(f"""
        <div class="stat-card stat-coral">
            <div class="stat-icon">🛠</div>
            <div class="stat-number">{stats['complaints_count']}</div>
            <div class="stat-label">Complaints</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛠", key="stat_complaints", use_container_width=True):
            st.switch_page("pages/complaint_portal.py")
    
    with s7:
        st.markdown(f"""
        <div class="stat-card stat-mint">
            <div class="stat-icon">🏠</div>
            <div class="stat-number">{stats['marketplace_count']}</div>
            <div class="stat-label">Marketplace</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏠", key="stat_marketplace", use_container_width=True):
            st.switch_page("pages/hostel_marketplace.py")
    
    with s8:
        st.markdown(f"""
        <div class="stat-card stat-sky">
            <div class="stat-icon">💼</div>
            <div class="stat-number">{stats['internship_count']}</div>
            <div class="stat-label">Internships</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💼", key="stat_internships", use_container_width=True):
            st.switch_page("pages/internship_board.py")
    
    with s9:
        st.markdown(f"""
        <div class="stat-card stat-blush">
            <div class="stat-icon">👨‍🏫</div>
            <div class="stat-number">{stats['mentor_count']}</div>
            <div class="stat-label">Mentors</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👨‍🏫", key="stat_mentors", use_container_width=True):
            st.switch_page("pages/mentor_matching.py")
    
    with s10:
        st.markdown(f"""
        <div class="stat-card stat-peach">
            <div class="stat-icon">🧪</div>
            <div class="stat-number">{stats['equipment_count']}</div>
            <div class="stat-label">Equipment</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🧪", key="stat_equipment", use_container_width=True):
            st.switch_page("pages/equipment_booking.py")
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# FOOTER

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown('<div class="footer-text">🎓 CampusConnect | Smart Campus Management System</div>', unsafe_allow_html=True)