import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os

def sendmail(
    receiver_email="",
    text="Anbei finden Sie Ihren Bericht",
    path="",
    subject = "",
):
    sender_email = os.environ.get("sender_email")
    server = os.environ.get("server")
    password = os.environ.get("mail_password")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    
    
    # open the file in bynary
    binary_pdf = open(path, 'rb')
    
    payload = MIMEBase('application', 'octate-stream', Name="report.pdf")
    payload.set_payload((binary_pdf).read())
    binary_pdf.close()
    
    # enconding the binary into base64
    encoders.encode_base64(payload)
    
    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename="report.pdf")
    message.attach(payload)
    

    # Create secure connection with server and send email
    with smtplib.SMTP_SSL(server, 465) as smtp_server:
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(sender_email, receiver_email, message.as_string())
