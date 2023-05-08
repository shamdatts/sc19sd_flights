from flights.models import Flight, Seat
from django.core.management.base import BaseCommand
import datetime
import random

# run using python manage.py records
class Command(BaseCommand):
    help = "Generates and saves flights"

    def handle(self, *args, **options):

        self.flight_generator()

        self.stdout.write(
            self.style.SUCCESS("Successfully created flights")
        )

    def flight_generator(self):

        start_date = datetime.datetime(2023, 5, 12)
        end_date = start_date + datetime.timedelta(days=30)
        locations = ["LBA", "BHD", "IPC", "CCU", "DXB", "SYD"]
        airport_pairs = [(a1, a2) for a1 in locations for a2 in locations if a1 != a2]


        # iterate through each day in next month
        for current_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days)):
            for departureAirport, destinationAirport in airport_pairs:
                departureTime = datetime.time(hour=random.randint(5, 23), minute=random.choice([00, 15, 30, 45]))
                duration = random.choice([1, 2, 3, 4])

                departureTime = datetime.datetime.combine(current_date, departureTime)
                arrivalTime = departureTime + datetime.timedelta(hours=duration)

                flight_data = {
                    "planeModel": "Boeing 747",
                    "numberOfRows": 35,
                    "seatsPerRow": 6,
                    "departureTime": departureTime,
                    "arrivalTime": arrivalTime,
                    "departureAirport": departureAirport,
                    "destinationAirport": destinationAirport
                }
                flight = Flight.objects.create(**flight_data)

                seats = flight.numberOfRows * flight.seatsPerRow
                for i in range(seats):
                    seat_data = {
                        "flightId": flight,
                        "seatNumber": i + 1,
                        "seatPrice": 45
                    }

                    Seat.objects.create(**seat_data)
