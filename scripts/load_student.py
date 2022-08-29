from orientationSystem.models import Bachelier
import csv


def run():
    with open('orientationSystem\data\student_information2.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Bachelier.objects.all().delete()

        for row in reader:
            print(row)
            student=  Bachelier.objects.create(matricule=row[1],serie_bac=row[2],wilaya_bac=row[3],moyenne_bac=row[4],
                                               sexe=row[5],english=row[6],french=row[7],his_geo=row[8],
                                               arabic_literature=row[9],maths=row[10],physics=row[11],
                                               philosophy=row[12],primary_module=row[13],islamic_science=row[14])
                                               

            student.save()