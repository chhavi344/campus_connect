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

if st.button(
    "Post Item",
    use_container_width=True
):

    if item_name.strip() == "":
        st.error("Enter Item Name")

    elif price.strip() == "":
        st.error("Enter Price")

    elif description.strip() == "":
        st.error("Enter Description")

    else:

        image_path = ""

        if image is not None:

            image_path = os.path.join(
                UPLOAD_FOLDER,
                image.name
            )

            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO marketplace
            (
                user_id,
                item_name,
                category,
                price,
                description,
                image_path
            )
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
        # =====================================================
# DASHBOARD & LOGOUT
# =====================================================

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

st.divider()

# =====================================================
# SEARCH ITEMS
# =====================================================

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
        u.full_name
    FROM marketplace m
    LEFT JOIN users u
    ON m.user_id=u.user_id
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

if len(items) == 0:

    if search.strip() != "":
        st.error("❌ Item Not Found")

    else:
        st.info("No Items Available")

else:

    for item in items:

        with st.container(border=True):

            c1, c2 = st.columns([1,3])

            with c1:

                if item["image_path"]:

                    if os.path.exists(item["image_path"]):

                        st.image(
                            item["image_path"],
                            width=180
                        )

            with c2:

                st.subheader(item["item_name"])

                st.write("👤 Seller :", item["full_name"])

                st.write("📂 Category :", item["category"])

                st.write("💰 Price :", item["price"])

                st.write("📝 Description :")

                st.write(item["description"])

                st.write("📌 Status :", item["status"])

                st.write("📅 Posted :", item["created_at"])