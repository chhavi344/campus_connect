import streamlit as st
import mysql.connector
import bcrypt

st.set_page_config(
    page_title="Forgot Password",
    page_icon="🔑",
    layout="centered"
)

# DATABASE CONNECTION

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chhavi@27",          
        database="campusconnect"
    )

# PAGE

st.title("🔑 Forgot Password")
st.write("Reset your CampusConnect Password")

st.divider()

email = st.text_input("📧 Registered Email")

new_password = st.text_input(
    "🔒 New Password",
    type="password"
)

confirm_password = st.text_input(
    "🔒 Confirm Password",
    type="password"
)

st.write("")

# RESET PASSWORD 

if st.button("Reset Password", use_container_width=True):

    email = email.strip().lower()

    if not email:
        st.error("Please enter your registered email.")

    elif "@" not in email or "." not in email:
        st.error("Please enter a valid email.")

    elif not new_password:
        st.error("Please enter new password.")

    elif not confirm_password:
        st.error("Please confirm your password.")

    elif new_password != confirm_password:
        st.error("Passwords do not match.")

    else:

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Check Registered Email
            cursor.execute(
                "SELECT * FROM users WHERE email=%s",
                (email,)
            )

            user = cursor.fetchone()

            if user:

                # Hash Password
                hashed_password = bcrypt.hashpw(
                    new_password.encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")

                # Update Password
                cursor.execute(
                    """
                    UPDATE users
                    SET password=%s
                    WHERE email=%s
                    """,
                    (
                        hashed_password,
                        email
                    )
                )

                conn.commit()

                st.success("✅ Password Updated Successfully!")

                st.balloons()

                st.switch_page("pages/login.py")

            else:

                st.error("❌ This email is not registered.")

        except Exception as e:

            st.error(f"Database Error : {e}")

        finally:

            if "cursor" in locals():
                cursor.close()

            if "conn" in locals():
                conn.close()

st.divider()

if st.button("⬅ Back to Login", use_container_width=True):
    st.switch_page("pages/login.py")