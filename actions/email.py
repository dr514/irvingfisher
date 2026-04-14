# actions/email.py
# Handles sending email with file attachments via Gmail SMTP

import smtplib
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

# Gmail credentials from .env
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(to: str, subject: str, file_path: str) -> dict:
    """
    Sends an email with a file attachment via Gmail.
    Returns a dict with success status or error message.
    """

    # Validate file exists
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"Output file not found at: {file_path}"
        }

    # Validate credentials are set
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "error": "Gmail credentials missing from .env"
        }

    try:
        # Build email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText("See attached output from JimmySims.", "plain"))

        # Attach file
        filename = Path(file_path).name
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}"
            )
            msg.attach(part)

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to, msg.as_string())

        return {
            "success": True,
            "message": f"Email sent to {to} with attachment {filename}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }