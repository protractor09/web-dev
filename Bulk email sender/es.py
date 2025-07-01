import smtplib
from email.message import EmailMessage
import time
from email_validator import validate_email, EmailNotValidError
import re
import streamlit as st
import os
import mimetypes


#check email format
def is_valid_email(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False
    
def get_email_txt(file):
    content = file.read().decode('utf-8')  # Read file content
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(email_pattern, content)))  # Unique emails

#send emails
def logic(EMAIL_ADDRESS,EMAIL_PASSWORD,EMAIL_BODY,SUBJECT,emails,attachments=None):

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for line in emails:
            # Support optional name,email format
            if "," in line:
                name, email = map(str.strip, line.split(",", 1))
            else:
                email = line
                name = ""

            msg = EmailMessage()
            msg['Subject'] = SUBJECT
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg.set_content(EMAIL_BODY.format(name=name))
            if attachments:
                for file in attachments:
                    mime_type, _ = mimetypes.guess_type(file)
                    if mime_type:
                        maintype, subtype = mime_type.split('/')
                    else:
                        maintype, subtype = 'application', 'octet-stream'
                    
                    with open(file,"rb") as f:
                        file_data = f.read()
                        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=os.path.basename(file))

            # In logic() method:
            try:
                smtp.send_message(msg)
                print(f"✅ Sent email to {name} <{email}>")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to send to {email}: {e}")
