from django.core.management.base import BaseCommand
from flights.models import Seat

class Command(BaseCommand):
    help = 'Resets all SeatTaken values to False'

    def handle(self, *args, **options):
        seats = Seat.objects.all()
        for seat in seats:
            seat.seatTaken = False
            seat.save()
        self.stdout.write(self.style.SUCCESS('Successfully reset all SeatTaken values.'))
