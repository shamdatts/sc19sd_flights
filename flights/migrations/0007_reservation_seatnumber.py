# Generated by Django 4.1.7 on 2023-05-09 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_alter_seat_seattaken'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='seatNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
