import streamlit as st
import os
from database import get_connection

st.set_page_config(
    page_title="Hostel Marketplace",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Hostel Marketplace")
st.caption("Buy & Sell Items Inside Campus")

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")


# DELETE FUNCTION

def delete_marketplace_item(item_id, user_id):
    """Delete a marketplace item only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First check if user owns this item
        cursor.execute(
            "SELECT user_id FROM marketplace WHERE item_id = %s",
            (item_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            # Delete the item
            cursor.execute(
                "DELETE FROM marketplace WHERE item_id = %s AND user_id = %s",
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
        st.error(f"Error deleting item: {e}")
        return False

# UPLOAD FOLDER

UPLOAD_FOLDER = "uploads/marketplace"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# SELL ITEM

st.subheader("🛒 Sell an Item")

item_name = st.text_input("Item Name")
category = st.selectbox(
    "Category",
    [
        "Books",
        "Electronics",
        "Furniture",
        "Cycle",
        "Clothes",
        "Stationery",
        "Other"
    ]
)
price = st.text_input("Price")
description = st.text_area("Description")
image = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if st.button("Post Item", use_container_width=True):
    if item_name.strip() == "":
        st.error("Enter Item Name")
    elif price.strip() == "":
        st.error("Enter Price")
    elif description.strip() == "":
        st.error("Enter Description")
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
            INSERT INTO marketplace
            (user_id, item_name, category, price, description, image_path)
            VALUES(%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state["user_id"],
                item_name,
                category,
                price,
                description,
                image_path
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Item Posted Successfully")
        st.balloons()
        st.rerun()

st.divider()


# NAVIGATION BUTTONS

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()


# AVAILABLE ITEMS WITH DELETE BUTTON

st.subheader("🛍 Available Items")

search = st.text_input(
    "🔍 Search Item",
    placeholder="Search by Item Name or Category"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        m.*,
        u.full_name,
        u.user_id as owner_id
    FROM marketplace m
    LEFT JOIN users u
    ON m.user_id = u.user_id
    WHERE
        m.item_name LIKE %s
        OR
        m.category LIKE %s
    ORDER BY m.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%"
    )
)

items = cursor.fetchall()
cursor.close()
conn.close()

if len(items) == 0:
    if search.strip() != "":
        st.error("❌ Item Not Found")
    else:
        st.info("No Items Available")
else:
    for item in items:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if item["image_path"]:
                    if os.path.exists(item["image_path"]):
                        st.image(item["image_path"], width=150)

            with col2:
                st.subheader(item["item_name"])
                st.write("📂 Category :", item["category"])
                st.write("💰 Price : ₹", item["price"])
                st.write("📝 Description :")
                st.write(item["description"])
                st.write("📌 Status :", item["status"])
                st.write("📅 Posted :", item["created_at"])
                
                # Show who posted
                st.caption(f"👤 Seller: {item['full_name']}")

            with col3:
                
                # DELETE BUTTON - Only for post owner
            
                if st.session_state.get('user_id') == item['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_marketplace_{item['item_id']}",
                        use_container_width=True
                    ):
                        if delete_marketplace_item(item['item_id'], st.session_state['user_id']):
                            st.success("✅ Item deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete item")
                else:
                    st.info("🔒 Item by other user")

st.divider()
st.caption("🏠 CampusConnect | Hostel Marketplace")