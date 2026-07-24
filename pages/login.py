import streamlit as st
import bcrypt
from database import get_connection

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Login")
st.caption("Welcome Back to CampusConnect")

st.divider()

# LOGIN FORM 

with st.form("login_form"):

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    login = st.form_submit_button(
        "Login",
        use_container_width=True
    )

# LOGIN 

if login:

    email = email.strip().lower()

    if email == "":

        st.error("Please enter Email.")

    elif password == "":

        st.error("Please enter Password.")

    else:

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email=%s
                """,
                (email,)
            )

            user = cursor.fetchone()

            if user is None:

                st.error("Email is not registered.")

            else:
                if bcrypt.checkpw(
                   password.encode("utf-8"),
                   user["password"].encode("utf-8")
                ):
                # Login Success
                    # SESSION 

                    st.session_state.logged_in = True
                    st.session_state.user_id = user["user_id"]
                    st.session_state.full_name = user["full_name"]
                    st.session_state.email = user["email"]

                    st.success("✅ Login Successful")

                    st.switch_page("pages/dashboard.py")

                else:

                    st.error("Incorrect Password.")

        except Exception as e:

            st.error(f"Database Error : {e}")

        finally:

            if "cursor" in locals():
                cursor.close()

            if "conn" in locals():
                conn.close()

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "📝 Create Account",
        use_container_width=True
    ):

        st.switch_page("pages/signup.py")

with col2:

    if st.button(
        "🔑 Forgot Password",
        use_container_width=True
    ):

        st.switch_page("pages/forgot_password.py")