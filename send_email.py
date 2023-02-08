import json
import smtplib
import ssl
import time
from email.mime.text import MIMEText

# The email address and password of the sender
sender_email = "fedora20050512@gmail.com"
sender_password = "qbzauhjidezlflht"
# sender_password = "mPAfnxhyTqKRA4mE3kFV"

# The email address of the recipient
recipient_email = "maijor18@mail.ru"
# recipient_email = "fiksuly2011@mail.ru"

# The subject and body of the email
subject = "Статьи изменились"


# Construct the MIME message
def create_letter():
    with open('all_categories_test.json', 'r', encoding='utf-8') as file:
        data = file.read()
    data = json.loads(data)

    # Serialize the dictionary to JSON
    json_data = json.dumps(data, ensure_ascii=False)
    message = MIMEText(json_data, 'plain')
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    # Send the email using the SMTP server of the sender's email provider
    context = ssl.create_default_context()
    article_date = 3

    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

