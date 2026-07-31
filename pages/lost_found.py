from notification_service import notify_all_users
import threading
import streamlit as st
import os
from datetime import date
from database import get_connection

st.set_page_config(
    page_title="Lost & Found",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Campus Lost & Found")
st.caption("Report Lost or Found Items")

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

UPLOAD_FOLDER = "uploads/lost_items"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# DELETE FUNCTIONS

def delete_lost_item(item_id, user_id):
    """Delete a lost item only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id FROM lost_items WHERE lost_id = %s",
            (item_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            cursor.execute(
                "DELETE FROM lost_items WHERE lost_id = %s AND user_id = %s",
                (item_id, user_id)
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
        st.error(f"Error deleting lost item: {e}")
        return False

def delete_found_item(item_id, user_id):
    """Delete a found item only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id FROM found_items WHERE found_id = %s",
            (item_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            cursor.execute(
                "DELETE FROM found_items WHERE found_id = %s AND user_id = %s",
                (item_id, user_id)
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
        st.error(f"Error deleting found item: {e}")
        return False


# TABS

lost_tab, found_tab = st.tabs(
    [
        "🔴 Report Lost Item",
        "🟢 Report Found Item"
    ]
)

with lost_tab:
    st.subheader("Report Lost Item")

    item_name = st.text_input("Item Name", key="lost_item")
    category = st.selectbox(
        "Category",
        ["Wallet", "Mobile", "Laptop", "Bag", "Book", "Keys", "ID Card", "Other"],
        key="lost_category"
    )
    description = st.text_area("Description", key="lost_description")
    location = st.text_input("Lost Location", key="lost_location")
    lost_date = st.date_input("Lost Date", value=date.today(), key="lost_date")
    image = st.file_uploader("Upload Image", type=["jpg","jpeg","png"], key="lost_image")

    if st.button("Submit Lost Item", key="submit_lost"):
        if item_name.strip() == "":
            st.error("Enter Item Name")
        elif description.strip() == "":
            st.error("Enter Description")
        elif location.strip() == "":
            st.error("Enter Location")
        else:
            image_path=""
            if image is not None:
                image_path=os.path.join(UPLOAD_FOLDER, image.name)
                with open(image_path,"wb") as f:
                    f.write(image.getbuffer())

            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute(
                """
                INSERT INTO lost_items
                (user_id, item_name, category, description, location, lost_date, image_path)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    st.session_state.get("user_id"),
                    item_name,
                    category,
                    description,
                    location,
                    lost_date,
                    image_path
                )
            )
            conn.commit()
            cursor.close()
            conn.close()

            threading.Thread(
                target=notify_all_users,
                args=(
                    "🔴 New Lost Item Reported",
                    f"""
Hello,

A new Lost Item has been reported.

📦 Item : {item_name}
📂 Category : {category}
📍 Location : {location}
📅 Date : {lost_date}

Login to CampusConnect to view details.

Regards,
CampusConnect Team
"""
                ),
                daemon=True
            ).start()

            st.success("✅ Lost Item Submitted Successfully")
            st.rerun()
            
with found_tab:
    st.subheader("Report Found Item")

    item_name = st.text_input("Item Name", key="found_item")
    category = st.selectbox(
        "Category",
        ["Wallet", "Mobile", "Laptop", "Bag", "Book", "Keys", "ID Card", "Other"],
        key="found_category"
    )
    description = st.text_area("Description", key="found_description")
    location = st.text_input("Found Location", key="found_location")
    found_date = st.date_input("Found Date", value=date.today(), key="found_date")
    image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="found_image")

    if st.button("Submit Found Item", key="submit_found"):
        if item_name.strip() == "":
            st.error("Enter Item Name")
        elif description.strip() == "":
            st.error("Enter Description")
        elif location.strip() == "":
            st.error("Enter Location")
        else:
            image_path = ""
            if image is not None:
                image_path = os.path.join(UPLOAD_FOLDER, image.name)
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO found_items
                (user_id, item_name, category, description, location, found_date, image_path)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    st.session_state.get("user_id"),
                    item_name,
                    category,
                    description,
                    location,
                    found_date,
                    image_path
                )
            )
            conn.commit()
            cursor.close()
            conn.close()

            threading.Thread(
                target=notify_all_users,
                args=(
                    "🟢 New Found Item Reported",
                    f"""
Hello,

A new Found Item has been reported.

📦 Item : {item_name}
📂 Category : {category}
📍 Location : {location}
📅 Date : {found_date}

Login to CampusConnect to view details.

Regards,
CampusConnect Team
"""
                ),
                daemon=True
            ).start()

            st.success("✅ Found Item Submitted Successfully")
            st.rerun()

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.divider()


# ALL LOST ITEMS WITH DELETE BUTTON

st.subheader("📍 All Lost Items")

search_lost = st.text_input(
    "🔍 Search Lost Item",
    placeholder="Search by Item Name or Category"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        l.*,
        u.full_name,
        u.user_id as owner_id
    FROM lost_items l
    LEFT JOIN users u
    ON l.user_id = u.user_id
    WHERE
        l.item_name LIKE %s
        OR
        l.category LIKE %s
    ORDER BY l.created_at DESC
    """,
    (
        "%" + search_lost + "%",
        "%" + search_lost + "%"
    )
)

lost_items = cursor.fetchall()
cursor.close()
conn.close()

if len(lost_items) == 0:
    if search_lost.strip() != "":
        st.error("❌ Item Not Found")
    else:
        st.info("No Lost Items Found")
else:
    for item in lost_items:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if item["image_path"]:
                    if os.path.exists(item["image_path"]):
                        st.image(item["image_path"], width=150)

            with col2:
                st.subheader(item["item_name"])
                st.write("📦 Category :", item["category"])
                st.write("📝 Description :", item["description"])
                st.write("📍 Location :", item["location"])
                st.write("📅 Lost Date :", item["lost_date"])
                st.write("🔎 Status :", item["status"])
                st.caption(f"👤 Posted By: {item['full_name']}")

            with col3:
                
                if st.session_state.get('user_id') == item['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_lost_{item['lost_id']}",
                        use_container_width=True
                    ):
                        if delete_lost_item(item['lost_id'], st.session_state['user_id']):
                            st.success("✅ Lost item deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete lost item")
                else:
                    st.info("🔒 Post by other user")

st.divider()


# ALL FOUND ITEMS WITH DELETE BUTTON

st.subheader("✅ All Found Items")

search_found = st.text_input(
    "🔍 Search Found Item",
    placeholder="Search by Item Name or Category"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        f.*,
        u.full_name,
        u.user_id as owner_id
    FROM found_items f
    LEFT JOIN users u
    ON f.user_id = u.user_id
    WHERE
        f.item_name LIKE %s
        OR
        f.category LIKE %s
    ORDER BY f.created_at DESC
    """,
    (
        "%" + search_found + "%",
        "%" + search_found + "%"
    )
)

found_items = cursor.fetchall()
cursor.close()
conn.close()

if len(found_items) == 0:
    if search_found.strip() != "":
        st.error("❌ Item Not Found")
    else:
        st.info("No Found Items Available")
else:
    for item in found_items:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if item["image_path"]:
                    if os.path.exists(item["image_path"]):
                        st.image(item["image_path"], width=150)

            with col2:
                st.subheader(item["item_name"])
                st.write("📦 Category :", item["category"])
                st.write("📝 Description :", item["description"])
                st.write("📍 Location :", item["location"])
                st.write("📅 Found Date :", item["found_date"])
                st.write("✅ Status :", item["status"])
                st.caption(f"👤 Posted By: {item['full_name']}")

            with col3:
                
                if st.session_state.get('user_id') == item['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_found_{item['found_id']}",
                        use_container_width=True
                    ):
                        if delete_found_item(item['found_id'], st.session_state['user_id']):
                            st.success("✅ Found item deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete found item")
                else:
                    st.info("🔒 Post by other user")

st.divider()


# LOGOUT

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()
st.caption("📍 CampusConnect | Lost & Found")