import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_sender.settings import EMAIL_PASSWORD, SENDER_EMAIL
from email_sender.db_connections import lifespan
from email_sender.settings import *
from email_sender.utils.utils import *
from pathlib import Path


def send_email(email: str, subject: str, template: str, link: str):
    try:
        current_year = datetime.now().year
        html_content = template.replace("{{ link }}", link).replace(
            "{{ year }}", str(current_year)
        )
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"Email sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def read_email_template(template_name: str) -> str:
    try:
        template_path = Path("email_sender") / template_name
        with open(template_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"Template {template_name} not found.")


def send_password_reset_email(email: str, token: str):
    try:
        reset_template = read_email_template("reset_password_email.html")
        reset_link = f"http://127.0.0.1:9090/reset_password?token={token}"
        send_email(email, "Password Reset", reset_template, reset_link)
    except Exception as e:
        print(f"Failed to send password reset email: {e}")


def send_verification_email(email: str, token: str):
    try:
        verification_template = read_email_template("verification_email.html")
        verification_link = f"http://127.0.0.1:9090/verify/{token}"
        send_email(
            email, "Email Verification", verification_template, verification_link
        )
    except Exception as e:
        print(f"Failed to send verification email: {e}")


def send_login_success_email(email: str, username: str, login_time: str):
    """Sends an email notification for successful login."""
    try:
        login_template = read_email_template("login_successful_email.html")
        current_year = datetime.now().year
        html_content = (
            login_template.replace("{{ username }}", username)
            .replace("{{ login_time }}", login_time)
            .replace("{{ year }}", str(current_year))
        )
        link = ""
        send_email(email, "Successful Login Notification", html_content, link)
    except Exception as e:
        print(f"Failed to send login success email: {e}")
