import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) 
    server = smtplib.SMTP('smtp.gmail.com', 587)    
    try: 
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
sender_email = "please write the sender email"
# "If you enable 2-step verification in Google, simply go to Google and search for 'App Password.' Create a new app, and it will give you a 16-digit password. Enter this password below."
sender_password = "please write the sender password"
receiver_email = "please write the reciver email"
subject = "Test Email"
body = "This is a test email sent from a Python script."

send_email(sender_email, sender_password, receiver_email, subject, body)


