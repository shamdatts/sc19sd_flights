from django.test import TestCase, Client
from datetime import datetime, date
from flights.models import FlightDetails, Passenger, Reservation, Seat
from django.utils import timezone
from django.core import serializers
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class QueryFlightsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #existing_flight = FlightDetails.objects.get(flightId=2149)
        FlightDetails.objects.create(
            planeModel='Boeing 747',
            numberOfRows=35,
            seatsPerRow=6,
            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
            departureAirport='BHD',
            destinationAirport='CCU'
        )
    
    def test_query_flights(self):
        response = self.client.get('/flights/query=2023-05-12&BHD&CCU/')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_date(self):
        response = self.client.get('/flights/query=2023-05&LBA&SYD/')
        self.assertEqual(response.status_code, 400)

    def test_no_flights_found(self):
        response = self.client.get('/flights/query=2023-05-04&LBA&SYD/')
        self.assertEqual(response.status_code, 404)

class CreateReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test objects
        self.flight = FlightDetails.objects.create(planeModel='Boeing 747',
                                            numberOfRows=35,
                                            seatsPerRow=6,
                                            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
                                            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
                                            departureAirport='BHD',
                                            destinationAirport='CCU')
        self.seat = Seat.objects.create(seatNumber='1', 
                                        seatPrice='45', 
                                        flightId=self.flight,
                                        seatTaken=False)
        self.json_data = {
            'passenger': {
                'firstName': 'John',
                'lastName': 'Doe',
                'dateOfBirth': '2000-01-01',
                'passportNumber': 12345678,
                'address': "1 London Road London LL1 0XX",
            },
            'seatNumber': self.seat.seatNumber,
            'holdLuggage': False,
            'paymentConfirmed': True,
            'flightId': self.flight.flightId,
        }
        self.url = reverse('create_reservation')                                                                    

        self.flight.save()
        self.seat.save()

    def test_create_reservation_success(self):
        url = reverse('create_reservation')
        # Update the seat to be available again
        self.seat.seatTaken = False
        self.seat.save()
        
        response = self.client.post(url, data=json.dumps(self.json_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify that the reservation was created
        reservation = Reservation.objects.get(seatNumber=self.seat.seatNumber, holdLuggage=False, paymentConfirmed=True )
        self.assertEqual(reservation.holdLuggage, False)
        self.assertEqual(reservation.paymentConfirmed, True)

    def test_create_reservation_missing_fields(self):
        json_data = {
            # Missing 'passenger' field
            'seatNumber': 'A1',
            'holdLuggage': False,
            'paymentConfirmed': True,
            'flightId': 1,
        }

        response = self.client.post(self.url, data=json.dumps(json_data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
    def test_create_reservation_invalid_ids(self):
        url = reverse('create_reservation')
        # Test with invalid passenger ID
        reservation_data = {
            'passenger': {
                'firstName': 'John',
                'lastName': 'Doe',
                'dateOfBirth': '2000-01-01',
                'passportNumber': 12345678,
                'address': "1 London Road London LL1 0XX",
            },
            'seatNumber': None,
            'holdLuggage': False,
            'paymentConfirmed': True,
            'flightId': self.flight.flightId,
        }
        response = self.client.post(url, data=json.dumps(reservation_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid flight ID
        reservation_data['flightId'] = self.flight.flightId + 100  # Invalid flight ID
        response = self.client.post(url, data=json.dumps(reservation_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid seat number for flight
        reservation_data['flightId'] = self.flight.flightId  # Reset flight ID
        reservation_data['seatNumber'] = None  # Invalid seat number
        response = self.client.post(url, data=json.dumps(reservation_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

class GetReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.flight = FlightDetails.objects.create(planeModel='Boeing 747',
                                            numberOfRows=35,
                                            seatsPerRow=6,
                                            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
                                            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
                                            departureAirport='BHD',
                                            destinationAirport='CCU')
        self.passenger = Passenger.objects.create(firstName='John', 
                                                  lastName='Doe', 
                                                  dateOfBirth=date(2000, 1, 1), 
                                                  passportNumber=12345678, 
                                                  address="1 London Road London LL1 0XX")
        self.seat = Seat.objects.create(seatNumber='1', 
                                        seatPrice='45', 
                                        flightId=self.flight)
        self.reservation = Reservation.objects.create(passengerId=self.passenger, 
                                                      seatId=self.seat, 
                                                      holdLuggage=False, 
                                                      paymentConfirmed=True) 

        self.flight.save()
        self.passenger.save()
        self.seat.save()
        self.reservation.save()

    def test_get_reservation_success(self):
        url = reverse('get_reservation', args=[self.reservation.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains the correct reservation data
        reservation_data = json.loads(response.content)
        self.assertEqual(reservation_data['holdLuggage'], False)
        self.assertEqual(reservation_data['paymentConfirmed'], True)

    def test_get_reservation_not_found(self):
        url = reverse('get_reservation', kwargs={'reservationId': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_get_reservation_wrong_method(self):
        url = reverse('get_reservation', args=[self.reservation.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 405)

class UpdateReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.flight = FlightDetails.objects.create(planeModel='Boeing 747',
                                            numberOfRows=35,
                                            seatsPerRow=6,
                                            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
                                            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
                                            departureAirport='BHD',
                                            destinationAirport='CCU')
        self.passenger = Passenger.objects.create(firstName='John', 
                                                  lastName='Doe', 
                                                  dateOfBirth=date(2000, 1, 1), 
                                                  passportNumber=12345678, 
                                                  address="1 London Road London LL1 0XX")
        self.seat = Seat.objects.create(seatNumber='1', 
                                        seatPrice='45', 
                                        flightId=self.flight,
                                        seatTaken=True)
        self.reservation = Reservation.objects.create(passengerId=self.passenger, 
                                                      seatId=self.seat, 
                                                      holdLuggage=False, 
                                                      paymentConfirmed=True) 

        self.flight.save()
        self.passenger.save()
        self.seat.save()
        self.reservation.save()

    def test_update_reservation(self):
        reservation_id = self.reservation.pk
        url = reverse('update_reservation', args=[reservation_id])
        request_body = {
            'seatId': self.seat.pk,
            'flightId': self.flight.pk,
            'passenger': {
                'passengerId': self.passenger.pk,
                'firstName': 'Jane',
                'lastName': 'Doe',
                'dateOfBirth': '1995-01-01',
                'passportNumber': '23456789',
                'address': '456 Street, City'
            },
            'holdLuggage': False,
            'paymentConfirmed': True
        }
        response = self.client.put(
            url,
            data=json.dumps(request_body),
            content_type='application/json'
        )
        print(response)
        self.assertEqual(response.status_code, 200)
        updated_reservation = Reservation.objects.get(pk=reservation_id)
        # Assert the updated values
        self.assertEqual(updated_reservation.seatId, self.seat)
        self.assertEqual(updated_reservation.passengerId, self.passenger)
        self.assertEqual(updated_reservation.holdLuggage, False)
        self.assertEqual(updated_reservation.paymentConfirmed, True)
        # Assert the updated passenger details
        updated_passenger = Passenger.objects.get(pk=self.passenger.pk)
        self.assertEqual(updated_passenger.firstName, 'Jane')
        self.assertEqual(updated_passenger.lastName, 'Doe')
        self.assertEqual(str(updated_passenger.dateOfBirth), '1995-01-01')
        self.assertEqual(str(updated_passenger.passportNumber), '23456789')
        self.assertEqual(updated_passenger.address, '456 Street, City')

    def test_update_reservation_seat_not_found(self):
        url = reverse('update_reservation', args=[self.reservation.pk])
        data = {
            'seatId': 1000,  # This ID doesn't exist
            'passenger': {
                'passengerId': self.passenger.pk,
                'firstName': 'John',
                'lastName': 'Doe',
                'dateOfBirth': '1990-01-01',
                'passportNumber': 'ABC123',
                'address': '123 Main St'
            },
            'holdLuggage': True,
            'paymentConfirmed': False
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_reservation_passenger_not_found(self):
        url = reverse('update_reservation', args=[self.reservation.pk])
        data = {
            'seatId': self.seat.pk,
            'passenger': {
                'passengerId': 1000,  # This ID doesn't exist
                'firstName': 'John',
                'lastName': 'Doe',
                'dateOfBirth': '1990-01-01',
                'passportNumber': 'ABC123',
                'address': '123 Main St'
            },
            'holdLuggage': True,
            'paymentConfirmed': False
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

class DeleteReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.flight = FlightDetails.objects.create(planeModel='Boeing 747',
                                            numberOfRows=35,
                                            seatsPerRow=6,
                                            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
                                            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
                                            departureAirport='BHD',
                                            destinationAirport='CCU')
        self.passenger = Passenger.objects.create(firstName='John', 
                                                  lastName='Doe', 
                                                  dateOfBirth=date(2000, 1, 1), 
                                                  passportNumber=12345678, 
                                                  address="1 London Road London LL1 0XX")
        self.seat = Seat.objects.create(seatNumber='1', 
                                        seatPrice='45', 
                                        flightId=self.flight)
        self.reservation = Reservation.objects.create(passengerId=self.passenger, 
                                                      seatId=self.seat, 
                                                      holdLuggage=False, 
                                                      paymentConfirmed=True) 

        self.flight.save()
        self.passenger.save()
        self.seat.save()
        self.reservation.save()

    def test_delete_reservation_success(self):
        response = self.client.delete(reverse('delete_reservation', kwargs={'reservationId': self.reservation.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(pk=self.reservation.pk).exists())

    def test_delete_reservation_not_found(self):
        response = self.client.delete(reverse('delete_reservation', kwargs={'reservationId': 999}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Reservation.objects.filter(pk=self.reservation.pk).exists())

    def test_delete_reservation_not_allowed(self):
        response = self.client.get(reverse('delete_reservation', kwargs={'reservationId': self.reservation.pk}))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Reservation.objects.filter(pk=self.reservation.pk).exists())


class ConfirmReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test objects
        self.flight = FlightDetails.objects.create(planeModel='Boeing 747',
                                            numberOfRows=35,
                                            seatsPerRow=6,
                                            departureTime=timezone.make_aware(datetime(2023, 5, 12, 5, 15)),
                                            arrivalTime=timezone.make_aware(datetime(2023, 5, 12, 8, 15)),
                                            departureAirport='BHD',
                                            destinationAirport='CCU')
        self.passenger = Passenger.objects.create(firstName='John', 
                                                  lastName='Doe', 
                                                  dateOfBirth=date(2000, 1, 1), 
                                                  passportNumber=12345678, 
                                                  address="1 London Road London LL1 0XX")
        self.seat = Seat.objects.create(seatNumber='1', 
                                        seatPrice='45', 
                                        flightId=self.flight,
                                        seatTaken=False)
        self.reservation = Reservation.objects.create(passengerId=self.passenger, 
                                                      seatId=self.seat, 
                                                      holdLuggage=False, 
                                                      paymentConfirmed=False) 
        self.flight.save()
        self.passenger.save()
        self.seat.save()
        self.reservation.save()

    def test_confirm_reservation_success(self):
        response = self.client.put(reverse('confirm_reservation', kwargs={'reservationId': self.reservation.pk}))
        self.assertEqual(response.status_code, 200)
        self.reservation.refresh_from_db()
        self.assertTrue(self.reservation.paymentConfirmed)

    def test_confirm_reservation_not_found(self):
        response = self.client.put(reverse('confirm_reservation', kwargs={'reservationId': 999}))
        self.assertEqual(response.status_code, 404)

    def test_confirm_reservation_not_allowed(self):
        response = self.client.get(reverse('confirm_reservation', kwargs={'reservationId': self.reservation.pk}))
        self.assertEqual(response.status_code, 405)