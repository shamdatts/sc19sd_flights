# sc19sd_flights

# Documentation:
username: ammar
password: university1

# URLS:
'flights/query=<str:date>&<str:departureAirport>&<str:destinationAirport>/': views.query_flights

'res/book/': views.create_reservation

'res/query=<int:reservationId>/': views.get_reservation

'res/update/query=<int:reservationId>/': views.update_reservation

'res/delete/query=<int:reservationId>/': views.delete_reservation

# Documentation:
https://app.swaggerhub.com/apis/LUKEMCDOWELL2014/FlightsAPI/1.0.0#/
