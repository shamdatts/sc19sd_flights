from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class FlightDetails(models.Model):
    flightId = models.AutoField(primary_key=True, editable=False)
    planeModel = models.CharField(max_length=255)
    numberOfRows = models.IntegerField()
    seatsPerRow = models.IntegerField()
    departureTime = models.DateTimeField()
    arrivalTime = models.DateTimeField()
    destinationAirport = models.CharField(max_length=255)
    departureAirport = models.CharField(max_length=255)

    class Meta:
        app_label = 'flights'

class Passenger(models.Model):
    passengerId = models.AutoField(primary_key=True, editable=False)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    passportNumber = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return str(self.pk)

class Seat(models.Model):
    seatId = models.AutoField(primary_key=True, editable=False)
    flightId = models.ForeignKey(FlightDetails, on_delete=models.CASCADE)
    seatNumber = models.IntegerField()
    seatPrice = models.DecimalField(decimal_places=2, max_digits=10)
    seatTaken = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

class Reservation(models.Model):
    reservationId = models.AutoField(primary_key=True, editable=False)
    seatId = models.ForeignKey(Seat, on_delete=models.DO_NOTHING)
    seatNumber = models.CharField(max_length=10, null=True, blank=True)
    passengerId = models.ForeignKey(Passenger, on_delete=models.DO_NOTHING)
    holdLuggage = models.BooleanField()
    paymentConfirmed = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.seatId:
            self.seatNumber = self.seatId.seatNumber
        super(Reservation, self).save(*args, **kwargs)