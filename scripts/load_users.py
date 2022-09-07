import os
import sys 
sys.path.append("C:\\Users\\AzurComputer\\Desktop\\PFE M2\\Project")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
import csv


def run():
    with open("orientationSystem/data/user.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        User.objects.all().delete() 
        for row in reader:
            print(row)
            print(len(row))
            user1=  User.objects.create_user(row[0], password=row[1])

            user1.save()