"""sc19sd_airline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    #path('flights/', views.all_flights, name='flights'),
    #path('flights/each_flight_details/<int:flight_id>', views.each_flight_details, name='each_flight_details'),
    path('flights/query=<str:date>&<str:departureAirport>&<str:destinationAirport>/', views.query_flights, name="query_flights"),
    #path('flights/query=<str:departureAirport>/<str:destinationAirport>/', views.query_flights, name="query_flights"),
    path('res/book/', views.create_reservation, name="create_reservation"),
    path('res/query=<int:reservationId>/', views.get_reservation, name="get_reservation"),
    path('res/update/query=<int:reservationId>/', views.update_reservation, name="update_reservation"),
    path('res/delete/query=<int:reservationId>/', views.delete_reservation, name="delete_reservation"),
    path('res/confirm/query=<int:reservationId>/', views.confirm_reservation, name="confirm_reservation"),
]