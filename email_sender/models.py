from django.db import models

class EmailRecord(models.Model):

    # Sender's email address
    sender = models.CharField(max_length=100)
    # Primary receiver(s); stored as comma-separated values for multiple recipients
    receiver = models.TextField()
    # Optional CC recipients; can be blank or null
    cc = models.TextField(blank=True, null=True)
    # Optional BCC recipients; can be blank or null
    bcc = models.TextField(blank=True, null=True)
    # Subject line of the email
    subject = models.CharField(max_length=255)
    # Body/content of the email message
    body = models.TextField()
    # Automatically set to the current date/time when the record is first created
    sent_at = models.DateTimeField(auto_now_add=True)
    # Email delivery status (e.g., "sent", "failed"); optional
    status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.subject}"
