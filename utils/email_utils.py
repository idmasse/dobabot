import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')

    # create email msg headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # create email msg body
    msg.attach(MIMEText(body, 'plain'))

    # connect to the server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("email sent successfully")
    except Exception as e:
        print(f"failed to send email: {e}")
    finally:
        server.quit()

def send_email_to_jarek(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    jareks_email = os.getenv('JAREKS_EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = jareks_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        text = msg.as_string()
        server.sendmail(sender_email, jareks_email, text)
        print("Email sent successfully to Jarek.")
    except Exception as e:
        print(f"Failed to send email to Jarek: {e}")
    finally:
        server.quit()