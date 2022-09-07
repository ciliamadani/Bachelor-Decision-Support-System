from orientationSystem.models import Bachelier
import csv
import os
import sys 
sys.path.append("C:\\Users\\AzurComputer\\Desktop\\PFE M2\\Project")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def run():
    with open('orientationSystem/data/student_information.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Bachelier.objects.all().delete()

        for row in reader:
            print(row)
            print(len(row))
            student=  Bachelier.objects.create(matricule=row[0],serie_bac=row[1],wilaya_bac=row[2],moyenne_bac=row[3],
                                               sexe=row[4],english=row[5],french=row[6],his_geo=row[7],
                                               arabic_literature=row[8],maths=row[9],physics=row[10],
                                               philosophy=row[11],primary_module=row[12],islamic_science=row[13])

            student.save()