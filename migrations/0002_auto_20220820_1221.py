# Generated by Django 3.2.5 on 2022-08-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orientationSystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bachelier',
            name='etablissement',
        ),
        migrations.RemoveField(
            model_name='bachelier',
            name='lieu_naissance',
        ),
        migrations.RemoveField(
            model_name='bachelier',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='bachelier',
            name='prenom',
        ),
        migrations.AddField(
            model_name='bachelier',
            name='arabic_literature',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='english',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='french',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='his_geo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='islamic_science',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='maths',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='philosophy',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='physics',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='primary_module',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='bachelier',
            name='sexe',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]
