# Generated by Django 4.1.7 on 2023-05-06 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='arrival_time',
            new_name='arrivalTime',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='destination',
            new_name='departureAirport',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='departure_time',
            new_name='departureTime',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='origin',
            new_name='destinationAirport',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='number_of_rows',
            new_name='numberOfRows',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='plane_model',
            new_name='planeModel',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='seats_per_row',
            new_name='seatsPerRow',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='DOB',
            new_name='dateOfBirth',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='passport_number',
            new_name='passportNumber',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='hold_luggage',
            new_name='holdLuggage',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='passenger_id',
            new_name='passengerId',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='payment_confirmed',
            new_name='paymentConfirmed',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='reservation_id',
            new_name='reservationId',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='seat_id',
            new_name='seatId',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='flight_id',
            new_name='flightId',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='seat_id',
            new_name='seatId',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='seat_number',
            new_name='seatNumber',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='seat_price',
            new_name='seatPrice',
        ),
    ]