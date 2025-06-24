import streamlit as st
import pandas as pd
import openpyxl
import email_sender as es
import tempfile

st.title("Bulk email sender")
st.warning("""
📌 **Please follow these instructions before using the app:**

1. The uploaded file must be in **.csv**, **.xlsx**, or **.txt** format.
2. The file must contain a column named exactly **email, emails, Email or Emails** .
3. Emails must be valid and properly formatted (e.g., `someone@example.com`).
4. Empty email cells will be skipped automatically.
5. Avoid using duplicate email addresses.
6. Do not exceed **500 emails per day** if using a Gmail account.
7. Review your content and email preview carefully before sending.
""")

st.info("""
🔐 **What is an App Password?**

Google no longer allows most apps (like this one) to use your regular Gmail password for security reasons.  
Instead, you must generate a **special one-time password** called an **App Password**.

### ✅ Steps to Get One:
1. Make sure 2-Step Verification is turned ON for your Gmail account.
2. Go to: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Choose:
   - App: **Mail**
   - Device: **Other (Windows Computer)** or anything
4. Google will generate a **16-character password**. Copy it.
5. Paste it into the app where it asks for your email password.

👉 **Note:** This is *not* your Gmail login password — and you don’t need to remember it.
""")

allowed_types = [
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "txt", "rtf", "csv", "jpg", "jpeg", "png", "gif",
    "mp3", "wav", "mp4", "mov", "avi", "mkv", "zip"
]

#initial information
email=st.text_input("Your email" ,key="user_email")
password=st.text_input("Your app password" , type="password" , key="user_pass")
subject=st.text_input("Subject of the email")
email_body=st.text_area("Enter email body here")
attach_file=st.file_uploader("Attach files (Optional)" , type=allowed_types , accept_multiple_files=True)

#selecting filetype
file_type=st.selectbox(
        'File format for emails:',
        ['csv or excel','text']
)

email_send=[]

#uploading emails list file
if file_type == 'csv or excel':
    csv_upload=st.file_uploader("Upload recipient list (.csv or .xlsx)",type=['csv','xlsx'])
    if csv_upload:
        try:
            if csv_upload.name.endswith('.csv'):
                df=pd.read_csv(csv_upload)
            else:
                df=pd.read_excel(csv_upload)

            st.write(df.head())

            required_cols = ['email', 'emails', 'Email', 'Emails']
            # Find which valid column exists
            valid_email_col = None
            for col in required_cols:
                if col in df.columns:
                    valid_email_col = col
                    break
                
            if valid_email_col:
                for _, row in df.iterrows():
                    email_value = str(row[valid_email_col]).strip()
                    if es.is_valid_email(email_value):
                        email_send.append(email_value)
                if not email_send:
                    st.warning("No valid emails found in the file.")
            else:
                st.error("File must contain at least one column named: 'email', 'emails', 'Email', or 'Emails'")

                
        except Exception as e:
            st.error(f"Failed to read the file: {e}")

if file_type == 'text':
    txt_upload=st.file_uploader("Upload recipient list (.txt)",type='txt')
    if txt_upload is not None:
        email_send=es.get_email_txt(file=txt_upload)
        st.write(email_send)
    else:
        st.warning("Upload a .txt file to continue")
    


confirm=st.checkbox("**Ready to Send? Click to Confirm**")


b=st.button("Send")

temp_path=[]

if attach_file:
    # Save the file to a temporary location
    for i in attach_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=i.name) as tmp_file:
            tmp_file.write(i.read())
            temp_path.append(tmp_file.name)

if confirm:
    if b:
        if not email or not password or not subject or not email_body:
            st.error("Please fill all the fields before sending emails.")
        elif not email_send:
            st.error("No valid recipients to send email to.")
        else:
            es.logic(email,password,email_body,subject,email_send,temp_path)

else:
    st.warning("confirm you want send the emails")