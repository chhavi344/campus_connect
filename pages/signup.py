import streamlit as st
from email_service import send_email
import bcrypt
from database import get_connection

st.set_page_config(
    page_title="Sign Up",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Create Your Account")
st.caption("Join CampusConnect")

st.divider()

# SIGNUP FORM 

with st.form("signup_form"):

    full_name = st.text_input("👤 Full Name")

    email = st.text_input("📧 Email")

    phone = st.text_input("📱 Phone Number")

    department = st.text_input("🏫 Department")

    semester = st.selectbox(
        "📚 Semester",
        [
            "Semester 1",
            "Semester 2",
            "Semester 3",
            "Semester 4",
            "Semester 5",
            "Semester 6",
            "Semester 7",
            "Semester 8"
        ]
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    confirm_password = st.text_input(
        "🔒 Confirm Password",
        type="password"
    )

    submit = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )

# CREATE ACCOUNT

if submit:

    full_name = full_name.strip()
    email = email.strip().lower()
    phone = phone.strip()
    department = department.strip()

    # Validation

    if full_name == "":
        st.error("Please enter Full Name.")

    elif email == "":
        st.error("Please enter Email.")

    elif "@" not in email or "." not in email:
        st.error("Please enter a valid Email Address.")

    elif phone == "":
        st.error("Please enter Phone Number.")

    elif not phone.isdigit():
        st.error("Phone Number should contain only digits.")

    elif department == "":
        st.error("Please enter Department.")

    elif password == "":
        st.error("Please enter Password.")

    elif confirm_password == "":
        st.error("Please confirm Password.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:

        try:

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Check Email

            cursor.execute(
                "SELECT user_id FROM users WHERE email=%s",
                (email,)
            )

            if cursor.fetchone():

                st.error("Email already registered.")

            else:

                # Check Phone

                cursor.execute(
                    "SELECT user_id FROM users WHERE phone=%s",
                    (phone,)
                )

                if cursor.fetchone():

                    st.error("Phone Number already registered.")

                else:

                    hashed_password = bcrypt.hashpw(
                        password.encode(),
                        bcrypt.gensalt()
                    ).decode()

                    cursor.execute(
                        """
                        INSERT INTO users
                        (
                            full_name,
                            email,
                            phone,
                            password,
                            department,
                            semester
                        )
                        VALUES
                        (
                            %s,%s,%s,%s,%s,%s
                        )
                        """,
                        (
                            full_name,
                            email,
                            phone,
                            hashed_password,
                            department,
                            semester
                        )
                    )
                    conn.commit()

                    # Send Welcome Email
                    send_email(
                        email,
                        "🎉 Welcome to CampusConnect",
                        f"""
Hello {full_name},

Welcome to CampusConnect!

Your account has been created successfully.

You can now use:

🚗 Ride Sharing
📚 Notes Sharing
🧪 Equipment Booking
🏠 Hostel Marketplace
🎉 Club Events

We hope you enjoy using CampusConnect.

Regards,
CampusConnect Team
"""
                    )

                    st.success("🎉 Account Created Successfully!")

                                      
                    st.balloons()

                    st.switch_page("pages/login.py")

        except Exception as e:

            st.error(f"Database Error: {e}")

        finally:

            if "cursor" in locals():
                cursor.close()

            if "conn" in locals():
                conn.close()