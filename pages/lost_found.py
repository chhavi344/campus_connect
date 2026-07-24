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

# login check 

if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

# create folder

UPLOAD_FOLDER = "uploads/lost_items"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# tabs

lost_tab, found_tab = st.tabs(
    [
        "🔴 Report Lost Item",
        "🟢 Report Found Item"
    ]
)

# lost items

with lost_tab:

    st.subheader("Report Lost Item")

    item_name = st.text_input(
        "Item Name",
        key="lost_item"
    )

    category = st.selectbox(
        "Category",
        [
            "Wallet",
            "Mobile",
            "Laptop",
            "Bag",
            "Book",
            "Keys",
            "ID Card",
            "Other"
        ],
        key="lost_category"
    )

    description = st.text_area(
        "Description",
        key="lost_description"
    )

    location = st.text_input(
        "Lost Location",
        key="lost_location"
    )

    lost_date = st.date_input(
        "Lost Date",
        value=date.today(),
        key="lost_date"
    )

    image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        key="lost_image"
    )

    if st.button(
        "Submit Lost Item",
        key="submit_lost"
    ):

        if item_name.strip() == "":
            st.error("Enter Item Name")

        elif description.strip() == "":
            st.error("Enter Description")

        elif location.strip() == "":
            st.error("Enter Location")

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
                INSERT INTO lost_items
                (
                    user_id,
                    item_name,
                    category,
                    description,
                    location,
                    lost_date,
                    image_path
                )
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

            st.success("Lost Item Submitted Successfully")

# found items

with found_tab:

    st.subheader("Report Found Item")

    item_name = st.text_input(
        "Item Name",
        key="found_item"
    )

    category = st.selectbox(
        "Category",
        [
            "Wallet",
            "Mobile",
            "Laptop",
            "Bag",
            "Book",
            "Keys",
            "ID Card",
            "Other"
        ],
        key="found_category"
    )

    description = st.text_area(
        "Description",
        key="found_description"
    )

    location = st.text_input(
        "Found Location",
        key="found_location"
    )

    found_date = st.date_input(
        "Found Date",
        value=date.today(),
        key="found_date"
    )

    image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        key="found_image"
    )

    if st.button(
        "Submit Found Item",
        key="submit_found"
    ):

        if item_name.strip() == "":
            st.error("Enter Item Name")

        elif description.strip() == "":
            st.error("Enter Description")

        elif location.strip() == "":
            st.error("Enter Location")

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
                INSERT INTO found_items
                (
                    user_id,
                    item_name,
                    category,
                    description,
                    location,
                    found_date,
                    image_path
                )
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

            st.success("✅ Found Item Submitted Successfully")
            st.rerun()

# dashboard button

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

# lost items

st.divider()

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
        u.full_name
    FROM lost_items l
    LEFT JOIN users u
    ON l.user_id=u.user_id
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

if len(lost_items) == 0:

    if search_lost.strip() != "":
        st.error("❌ Item Not Found")
    else:
        st.info("No Lost Items Found")

else:

    for item in lost_items:

        with st.container(border=True):

            col1, col2 = st.columns([1,3])

            with col1:

                if item["image_path"]:

                    if os.path.exists(item["image_path"]):
                        st.image(
                            item["image_path"],
                            width=180
                        )

            with col2:

                st.subheader(item["item_name"])

                st.write("👤 Posted By :", item["full_name"])
                st.write("📦 Category :", item["category"])
                st.write("📝 Description :", item["description"])
                st.write("📍 Location :", item["location"])
                st.write("📅 Lost Date :", item["lost_date"])
                st.write("🔎 Status :", item["status"])

cursor.close()
conn.close()

# found items 

st.divider()

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
        u.full_name
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

if len(found_items) == 0:

    if search_found.strip() != "":
        st.error("❌ Item Not Found")

    else:
        st.info("No Found Items Available")

else:

    for item in found_items:

        with st.container(border=True):

            col1, col2 = st.columns([1,3])

            with col1:

                if item["image_path"]:

                    if os.path.exists(item["image_path"]):
                        st.image(
                            item["image_path"],
                            width=180
                        )

            with col2:

                st.subheader(item["item_name"])

                st.write("👤 Posted By :", item["full_name"])
                st.write("📦 Category :", item["category"])
                st.write("📝 Description :", item["description"])
                st.write("📍 Location :", item["location"])
                st.write("📅 Found Date :", item["found_date"])
                st.write("✅ Status :", item["status"])

cursor.close()
conn.close()

# logout 

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")
        