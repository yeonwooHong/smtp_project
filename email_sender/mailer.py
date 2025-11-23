import smtplib, ssl, certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

# Send an email using the provided sender credentials and recipient lists.
def send_email(email_sender, app_password, receiver_emails, cc_emails=None, bcc_emails=None, subject="", body="", filename=None):
    # Validate app password is provided
    if not app_password or not app_password.strip():
        raise ValueError("App password cannot be empty. Please provide a valid Gmail App Password.")
    
    # Remove spaces from app password (in case user copied with spaces)
    app_password = app_password.strip().replace(" ", "")
    
    # Ensure all are lists
    if not isinstance(receiver_emails, list):
        receiver_emails = [receiver_emails]
    if cc_emails is None:
        cc_emails = []
    elif not isinstance(cc_emails, list):
        cc_emails = [cc_emails]
    if bcc_emails is None:
        bcc_emails = []
    elif not isinstance(bcc_emails, list):
        bcc_emails = [bcc_emails]

    # Build the email message
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = ", ".join(receiver_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject

    # Attach the main text body
    msg.attach(MIMEText(body, "plain"))

    # Attach file if provided
    if filename:
        try:
            with open(filename, "rb") as f:
                part = MIMEApplication(f.read(), Name=basename(filename))
                part["Content-Disposition"] = f'attachment; filename="{basename(filename)}"'
                msg.attach(part)
        except FileNotFoundError:
            raise FileNotFoundError(f"Attachment file not found: {filename}")
        except Exception as e:
            raise Exception(f"Error reading attachment file: {e}")

    # Combine all recipients (To + CC + BCC)
    all_recipients = receiver_emails + cc_emails + bcc_emails

    # Send email using Gmail SMTP with SSL
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, app_password)  # Authenticate using app password
            smtp.sendmail(email_sender, all_recipients, msg.as_string())    # Send the full message
        print("\n Email sent successfully!\n")
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n✗ Authentication failed!")
        print(f"  Error: {str(e)}")
        print(f"  Most likely causes:")
        print(f"  1. You're using your regular password instead of an App Password")
        print(f"  2. The App Password is incorrect")
        print(f"  3. 2-Step Verification is not enabled (required for App Passwords)")
        print(f"  4. The App Password was revoked or expired")
        print(f"  → Get a new App Password at: https://myaccount.google.com/apppasswords\n")
        raise
    except smtplib.SMTPRecipientsRefused as e:
        print(f"\n✗ Failed to send email: Invalid recipient email address(es)")
        print(f"  Error: {str(e)}\n")
        raise
    except smtplib.SMTPException as e:
        print(f"\n✗ SMTP error occurred: {str(e)}\n")
        raise
    except Exception as e:
        print(f"\n✗ Failed to send email: {str(e)}\n")
        raise
