from django.urls import path, include
from rest_framework import routers
from .views import (RoomViewSet,
                    RoomCreateView,
                    ReservationViewSet,
                    ReserveView, 
                    ReservationDetailView, 
                    ReservationUpdateView)

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'reservations', ReservationViewSet, basename='reservations')

urlpatterns = [
    path('', include(router.urls)),
    path('create-room/', RoomCreateView.as_view(), name='create-room'),
    path('reserve/', ReserveView.as_view(), name='reserve'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
]