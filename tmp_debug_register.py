import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cinesmart.settings')
import django
django.setup()
from rest_framework.test import APIClient
c=APIClient()
r=c.post('/api/auth/register/', {'username':'u1','password':'pass12345','email':'a@b.c'}, format='json')
print('status', r.status_code)
print('data', r.data)
