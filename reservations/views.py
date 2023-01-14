from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from datetime import datetime
from django.conf import settings
import stripe

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class RoomCreateView(APIView):
    def post(self, request, format=None):
        room_id = request.data.get('room_id')
        capacity = request.data.get('capacity')
        price_per_day = request.data.get('price_per_day')

        if not all([room_id, capacity, price_per_day]):
            return Response({'error': 'room_id, capacity, and price_per_day are required'}, status=status.HTTP_400_BAD_REQUEST)

        # validate if room_id is integer
        if not isinstance(room_id, int):
            return Response({'error': 'room_id must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        #validate if room_id is unique
        if Room.objects.filter(room_id=room_id).exists():
            return Response({'error': 'room_id is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        #validate if room_id is positive
        if room_id < 0:
            return Response({'error': 'room_id must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

        #validate if capacity is positive
        if capacity < 0:
            return Response({'error': 'capacity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the required data is provided
        if not all([room_id, capacity, price_per_day]):
            return Response({'error': 'room_id, capacity, and price_per_day are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(capacity, int):
            return Response({'error': 'capacity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(price_per_day, float) or price_per_day < 0:
            return Response({'error': 'price_per_day must be a positive float'}, status=status.HTTP_400_BAD_REQUEST)


        # Create the room
        room = Room(room_id=room_id, capacity=capacity, price_per_day=price_per_day)
        room.save()

        # Serialize the room and return it
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReserveView(APIView):
    def post(self, request, format=None):
        room_id = request.data.get('room_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')

        # Validate that the required data is provided
        if not all([room_id, start_date, end_date, customer_name, customer_email]):
            return Response({'error': 'room_id, start_date, end_date, customer_name, and customer_email are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'The specified room does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # the dates are on string format, so we need to convert them to date format
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. The correct format is YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        # validate if start_date is before end_date and both are in the future
        if start_date > end_date or start_date < datetime.now().date() or end_date < datetime.now().date():
            return Response({'error': 'Invalid dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the room is available
        if Reservation.objects.filter(room=room, start_date__lte=end_date, end_date__gte=start_date).exists():
            return Response({'error': 'The room is not available for the specified dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the quantity of people is valid
        if room.capacity < Reservation.objects.filter(start_date__lte=end_date, end_date__gte=start_date).count():
            return Response({'error': 'The room is not available for the specified dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the reservation
        reservation = Reservation(room=room, start_date=start_date, end_date=end_date,
                                  customer_name=customer_name, customer_email=customer_email, status='pending')
        reservation.save()

        # Serialize the reservation and return it
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ReservationDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'The specified reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


class ReservationUpdateView(APIView):
    def post(self, request, pk, format=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'The specified reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        #validate that the data is correct
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')

        # validate if all the data is provided
        if not all([start_date, end_date, customer_name, customer_email]):
            return Response({'error': 'start_date, end_date, customer_name, and customer_email are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        # the dates are on string format, so we need to convert them to date format
        # before we do that, we need to validate that they are in the correct format
        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%d-%m').date()
                datetime.strptime(end_date, '%Y-%d-%m').date()
            except ValueError:
                return Response({'error': 'Invalid start_date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = datetime.strptime(start_date, '%Y-%d-%m').date()
        end_date = datetime.strptime(end_date, '%Y-%d-%m').date()

        # validate if start_date is before end_date and both are in the future
        if start_date > end_date or start_date < datetime.now().date() or end_date < datetime.now().date():
            return Response({'error': 'Invalid dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the room is available
        if Reservation.objects.filter(room=reservation.room, start_date__lte=end_date, end_date__gte=start_date).exists():
            return Response({'error': 'The room is not available for the specified dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the quantity of people is valid
        if reservation.room.capacity < Reservation.objects.filter(start_date__lte=end_date, end_date__gte=start_date).count():
            return Response({'error': 'The room is not available for the specified dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the reservation
        reservation.start_date = start_date
        reservation.end_date = end_date
        reservation.customer_name = customer_name
        reservation.customer_email = customer_email

        reservation.save()

        # Serialize the reservation and return it
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationDeleteView(APIView):
    def post(self, request, pk, format=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'The specified reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



########## PAYMENT VIEWS #############

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(APIView):
    def post(self, request):
        try:
            token = stripe.Token.create(
                card={
                    "number": request.data.get('number'),
                    "exp_month": request.data.get('exp_month'),
                    "exp_year": request.data.get('exp_year'),
                    "cvc": request.data.get('cvc'),
                },
            )
            return Response({"token": token.id}, status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            return Response({"error": e.json_body}, status=e.http_status)

        except stripe.error.InvalidRequestError as e:
            return Response({"error": e.json_body}, status=e.http_status)

        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


class PaymentChargeView(APIView):
    # This view is used to charge the customer and change the status of the reservation
    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'The specified reservation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            charge = stripe.Charge.create(
                amount=int(reservation.total_price * 100), # amount in cents
                currency="usd",
                source=request.data.get('token'),
                description="Charge for " + reservation.customer_email,
            )
            reservation.status = 'paid'
            reservation.save()
            return Response({"charge": charge}, status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            return Response({"error": e.json_body}, status=e.http_status)

        except stripe.error.InvalidRequestError as e:
            return Response({"error": e.json_body}, status=e.http_status)

        except Exception as e:
            return Response({"error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)