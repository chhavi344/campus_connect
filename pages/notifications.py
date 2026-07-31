
import streamlit as st
import os
from datetime import datetime
from database import get_connection

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")


# CUSTOM CSS

st.markdown("""
<style>
    .stApp {
        background-color: #f8f6fc !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .notification-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px 25px;
        margin: 15px 0;
        border: 1px solid #f0ebf8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    .notification-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.08);
        border-color: #d6cbf5;
    }

    .badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 10px;
        color: #fff;
    }
    .badge-Lost { background: #ff6b6b; }
    .badge-Found { background: #4ecdc4; }
    .badge-Book { background: #5f27cd; }
    .badge-Note { background: #f39c12; }
    .badge-Ride { background: #3498db; }
    .badge-Event { background: #e84393; }
    .badge-Internship { background: #00b894; }
    .badge-Complaint { background: #d63031; }
    .badge-Marketplace { background: #fdcb6e; color: #333; }
    .badge-Equipment { background: #6c5ce7; }
    .badge-Mentor { background: #00cec9; }

    .notification-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
    }
    .notification-detail {
        color: #555555;
        font-size: 14px;
        margin: 6px 0;
    }
    .notification-time {
        color: #888888;
        font-size: 12px;
    }

    /* User Section - Without Profile Picture */
    .notification-user {
        background: #faf8fd;
        padding: 10px 15px;
        border-radius: 12px;
        margin-top: 12px;
        border: 1px solid #f0ebf8;
    }

    .stDivider {
        margin: 10px 0 !important;
    }
    .block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# FETCH ALL POSTS

def get_all_posts():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        all_posts = []
        
        # Lost Items
        cursor.execute("""
            SELECT 'Lost' as type, 
                   CONCAT('📍 ', l.item_name) as title,
                   CONCAT('Category: ', l.category, ' | Location: ', l.location) as detail,
                   l.description,
                   CONCAT('Status: ', l.status) as status,
                   l.created_at,
                   u.full_name, u.email, u.phone
            FROM lost_items l
            LEFT JOIN users u ON l.user_id = u.user_id
            WHERE l.status != 'Found'
            ORDER BY l.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Found Items
        cursor.execute("""
            SELECT 'Found' as type, 
                   CONCAT('🔍 ', f.item_name) as title,
                   CONCAT('Category: ', f.category, ' | Location: ', f.location) as detail,
                   f.description,
                   CONCAT('Status: ', f.status) as status,
                   f.created_at,
                   u.full_name, u.email, u.phone
            FROM found_items f
            LEFT JOIN users u ON f.user_id = u.user_id
            WHERE f.status = 'Available'
            ORDER BY f.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Books
        cursor.execute("""
            SELECT 'Book' as type, 
                   CONCAT('📚 ', b.book_name) as title,
                   CONCAT('Author: ', b.author, ' | Subject: ', b.subject) as detail,
                   b.book_condition as description,
                   CONCAT('Status: ', b.status) as status,
                   b.created_at,
                   u.full_name, u.email, u.phone
            FROM books b
            LEFT JOIN users u ON b.user_id = u.user_id
            WHERE b.status = 'Available'
            ORDER BY b.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Notes
        cursor.execute("""
            SELECT 'Note' as type, 
                   CONCAT('📝 ', n.title) as title,
                   CONCAT('Subject: ', n.subject, ' | Semester: ', n.semester) as detail,
                   n.description,
                   '' as status,
                   n.created_at,
                   u.full_name, u.email, u.phone
            FROM notes n
            LEFT JOIN users u ON n.user_id = u.user_id
            ORDER BY n.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Rides
        cursor.execute("""
            SELECT 'Ride' as type, 
                   CONCAT('🚗 ', r.source, ' → ', r.destination) as title,
                   CONCAT('Date: ', r.ride_date, ' | Time: ', r.ride_time) as detail,
                   CONCAT('Seats: ', r.available_seats, ' | Vehicle: ', r.vehicle) as description,
                   CONCAT('Status: ', r.status) as status,
                   r.created_at,
                   u.full_name, u.email, u.phone
            FROM rides r
            LEFT JOIN users u ON r.user_id = u.user_id
            WHERE r.status = 'Available'
            ORDER BY r.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Events
        cursor.execute("""
            SELECT 'Event' as type, 
                   CONCAT('🎉 ', e.event_name) as title,
                   CONCAT('Venue: ', e.venue, ' | Date: ', e.event_date) as detail,
                   CONCAT('Time: ', e.event_time) as description,
                   '' as status,
                   e.created_at,
                   u.full_name, u.email, u.phone
            FROM events e
            LEFT JOIN users u ON e.user_id = u.user_id
            WHERE e.event_date >= CURDATE()
            ORDER BY e.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Internships
        cursor.execute("""
            SELECT 'Internship' as type, 
                   CONCAT('💼 ', i.company_name) as title,
                   CONCAT('Role: ', i.role, ' | Location: ', i.location) as detail,
                   CONCAT('Stipend: ', i.stipend) as description,
                   CONCAT('Last Date: ', i.last_date) as status,
                   i.created_at,
                   NULL as full_name, NULL as email, NULL as phone
            FROM internships i
            WHERE i.last_date >= CURDATE()
            ORDER BY i.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Complaints
        cursor.execute("""
            SELECT 'Complaint' as type, 
                   CONCAT('🛠 ', c.title) as title,
                   CONCAT('Category: ', c.category) as detail,
                   c.description,
                   CONCAT('Status: ', c.status) as status,
                   c.created_at,
                   u.full_name, u.email, u.phone
            FROM complaints c
            LEFT JOIN users u ON c.user_id = u.user_id
            ORDER BY c.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Marketplace
        cursor.execute("""
            SELECT 'Marketplace' as type, 
                   CONCAT('🏠 ', m.item_name) as title,
                   CONCAT('Category: ', m.category, ' | Price: ₹', m.price) as detail,
                   m.description,
                   CONCAT('Status: ', m.status) as status,
                   m.created_at,
                   u.full_name, u.email, u.phone
            FROM marketplace m
            LEFT JOIN users u ON m.user_id = u.user_id
            WHERE m.status = 'Available'
            ORDER BY m.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Equipment Bookings
        cursor.execute("""
            SELECT 'Equipment' as type, 
                   CONCAT('🧪 ', e.equipment_name) as title,
                   CONCAT('Category: ', e.category, ' | Quantity: ', e.quantity) as detail,
                   e.purpose as description,
                   CONCAT('Status: ', e.status) as status,
                   e.created_at,
                   u.full_name, u.email, u.phone
            FROM equipment_bookings e
            LEFT JOIN users u ON e.user_id = u.user_id
            ORDER BY e.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        # Mentors
        cursor.execute("""
            SELECT 'Mentor' as type, 
                   CONCAT('👨‍🏫 ', m.mentor_name) as title,
                   CONCAT('Department: ', m.department) as detail,
                   CONCAT('Skills: ', m.skills) as description,
                   CONCAT('Availability: ', m.availability) as status,
                   m.created_at,
                   u.full_name, u.email, u.phone
            FROM mentors m
            LEFT JOIN users u ON m.user_id = u.user_id
            ORDER BY m.created_at DESC
        """)
        for row in cursor.fetchall():
            all_posts.append(row)
        
        all_posts.sort(key=lambda x: x['created_at'], reverse=True)
        
        cursor.close()
        conn.close()
        
        return all_posts
        
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []

# SEARCH FUNCTION

def search_posts(posts, search_term):
    if not search_term:
        return posts
    search_term = search_term.lower()
    return [p for p in posts if 
            search_term in p['title'].lower() or 
            search_term in p['detail'].lower() or
            search_term in (p.get('description') or '').lower() or
            (p.get('full_name') and search_term in p['full_name'].lower())]


# MAIN PAGE

st.markdown("<h1 style='color: #4a154b;'>🔔 Notifications</h1>", unsafe_allow_html=True)

search = st.text_input(
    "🔍 Search Notifications",
    placeholder="Search by Title, Category, or User Name...",
    key="notification_search"
)

all_posts = get_all_posts()

if all_posts:
    st.info(f"📬 Total **{len(all_posts)}** Notifications")
    st.divider()
    
    if search:
        all_posts = search_posts(all_posts, search)
        if not all_posts:
            st.warning("No notifications found matching your search.")
            st.stop()
    
    for post in all_posts:
        badge_html = f'<span class="badge badge-{post["type"]}">{post["type"]}</span>'
        
        with st.container():
            st.markdown(f"""
            <div class="notification-card">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    {badge_html}
                    <span class="notification-title">{post['title']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if post.get('detail'):
                st.markdown(f'<div class="notification-detail">{post["detail"]}</div>', unsafe_allow_html=True)
            
            if post.get('description') and post['description']:
                st.markdown(f'<div class="notification-detail" style="color: #666;">{post["description"]}</div>', unsafe_allow_html=True)
            
            if post.get('status') and post['status']:
                st.markdown(f'<div class="notification-detail" style="color: #4a154b; font-weight: 500;">{post["status"]}</div>', unsafe_allow_html=True)
            
            date_str = post['created_at'].strftime('%d %B %Y, %I:%M %p')
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                    <div class="notification-time">🕒 {date_str}</div>
                </div>
            """, unsafe_allow_html=True)
            
            
            # USER SECTION - WITHOUT PROFILE PICTURE
            
            if post.get('full_name'):
                st.markdown(f"""
                <div class="notification-user">
                    <div>
                        <strong style="color: #1a1a1a;">👤 {post['full_name']}</strong><br>
                        <span style="color: #555; font-size: 13px;">📧 {post['email']} &nbsp;|&nbsp; 📞 {post['phone']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔔 No notifications available. Start by posting something!")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("👤 My Profile", use_container_width=True):
        st.switch_page("pages/profile.py")

st.markdown('<p style="text-align: center; color: #999999; font-size: 12px; margin-top: 10px;">🔔 CampusConnect | Notifications</p>', unsafe_allow_html=True)