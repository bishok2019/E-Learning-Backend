import os

import django
from django.contrib.auth import get_user_model

# create_admin.py
# Set Django settings module if not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_learning_backend.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(email_address="admin@example.com").exists():
    User.objects.create_superuser(email_address="admin@example.com", password="admin")
    print("Superuser created.")
else:
    print("Superuser already exists.")
