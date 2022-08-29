from django.contrib.auth.models import User
import csv


def run():
    with open("orientationSystem\\data\\users.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        User.objects.all().delete() 
        for row in reader:
            print(row)
            print(len(row))
            user1=  User.objects.create_user(row[1], password=row[2])

            user1.save()