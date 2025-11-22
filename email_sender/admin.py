from django.contrib import admin
from .models import EmailRecord
from .user import User

# Register your model so it appears in Django admin
admin.site.register(EmailRecord)
admin.site.register(User)
