# Generated by Django 4.1.7 on 2023-05-11 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0007_reservation_seatnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='seatNumber',
        ),
    ]
