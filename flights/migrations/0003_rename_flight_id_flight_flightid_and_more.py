# Generated by Django 4.1.7 on 2023-05-06 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_rename_arrival_time_flight_arrivaltime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='flight_id',
            new_name='flightId',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='passenger_id',
            new_name='passengerId',
        ),
    ]
