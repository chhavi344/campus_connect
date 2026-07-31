from database import get_connection
from email_service import send_email


def notify_all_users(subject, message):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT email FROM users")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    for user in users:

        try:

            send_email(
                user["email"],
                subject,
                message
            )

        except Exception as e:

            print(e)