import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


def send_email(from_email, to_email, attachment, subject, content, key):
    message = Mail(
        from_email=from_email, to_emails=to_email, subject=subject, html_content=content
    )

    with open(attachment, "rb") as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()
    attached_file = Attachment(
        FileContent(encoded_file),
        FileName(attachment),
        FileType("application/json"),
        Disposition("attachment"),
    )
    message.attachment = attached_file

    sg = SendGridAPIClient(key)
    response = sg.send(message)
    if response.status_code == 202:
        print("Emailed results to %s" % to_email)
    else:
        print("Failed to send email")
