#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'eslam'
email = 'eslam@example.com'
password = 'password123'

if User.objects.filter(username=username).exists():
    print(f"User {username} already exists!")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Eslam',
        last_name='Essam'
    )
    print(f"Superuser {username} created successfully!")
    print(f"Employee ID: {user.profile.employee_id}")
