from django.contrib import admin
from flights.models import FlightDetails, Passenger, Seat, Reservation

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flightId', 'planeModel', 'numberOfRows', 'seatsPerRow', 'departureTime', 'arrivalTime', 'destinationAirport', 'departureAirport')

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passengerId', 'firstName', 'lastName', 'dateOfBirth', 'passportNumber', 'address')

class SeatAdmin(admin.ModelAdmin):
    list_display = ('seatId', 'flightId', 'seatNumber', 'seatPrice')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservationId', 'seatId', 'passengerId', 'holdLuggage', 'paymentConfirmed')


admin.site.register(FlightDetails, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Reservation, ReservationAdmin)