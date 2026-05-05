import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("APP_PASSWORD")

def send_otp_email(destination: str, otp_code: str):
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = destination
    message["Subject"] = "Tu código de verificación"

    body = f"""
    <h2>Verificación de cuenta</h2>
    <p>Tu código de verificación es:</p>
    <h1 style="letter-spacing: 8px;">{otp_code}</h1>
    <p>Este código expira en 10 minutos.</p>
    """
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destination, message.as_string())
