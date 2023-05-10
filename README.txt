sc19sd_flights
PythonAnywhere domain: http://shamitadatta2.pythonanywhere.com/

Username and Password for http://shamitadatta2.pythonanywhere.com/admin/
username: ammar
password: university1

This is the Flights API that allows you to query flights, or book, update, get or delete reservations. 

The possible URLs are stated below:
admin/
flights/query=<str:date>&<str:departureAirport>&<str:destinationAirport>/ [name='query_flights']
res/book/ [name='create_reservation']
res/query=<int:reservationId>/ [name='get_reservation']
res/update/query=<int:reservationId>/ [name='update_reservation']
res/delete/query=<int:reservationId>/ [name='delete_reservation']

Documentation:
https://app.swaggerhub.com/apis/LUKEMCDOWELL2014/FlightsAPI/1.0.0#/
