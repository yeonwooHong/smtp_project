import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_project.settings")
django.setup()

from email_sender.models import EmailRecord

# Initialize the Django database connection.
def init_db():
    """
    Make sure you've run:
    python manage.py makemigrations
    python manage.py migrate
    """
    print("Django DB ready (run migrations if not done yet)")

# Save an email record to the Django database.
def save_email(sender, receivers, subject, body, cc=None, bcc=None, filename=None):

    # Convert lists of recipients into comma-separated strings
    receivers_str = ", ".join(receivers) if isinstance(receivers, list) else receivers
    cc_str = ", ".join(cc) if isinstance(cc, list) else (cc or "")
    bcc_str = ", ".join(bcc) if isinstance(bcc, list) else (bcc or "")

    # Create and save the record
    record = EmailRecord(
        sender=sender,
        receiver=receivers_str,
        cc=cc_str,
        bcc=bcc_str,
        subject=subject,
        body=body,
        filename=filename,
        status = 'sent'
    )
    record.save()
    print("Email saved to Django database")

# Retrieve all stored email records from the database.
def get_all_emails():

    # Retrieve all email records, ordered by newest first.
    return EmailRecord.objects.all().order_by('-sent_at')

def get_email_by_id(email_id):

    # Retrieve a single email record by its ID.
    try:
        return EmailRecord.objects.get(id=email_id)
    except EmailRecord.DoesNotExist:
        return None

