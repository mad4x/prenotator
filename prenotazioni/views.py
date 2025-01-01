from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from prenotazioni.models import Booking
from prenotazioni.serializers import BookingSerializer

@api_view(['GET'])
def listBookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addBooking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBooking(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"error":"prenotazione non trovata"}, status=404)

    booking.delete()
    return Response({"message":"prenotazione eliminata con successo"}, status=204)

@api_view(['PATCH'])
def updateBooking(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"error":"prenotazione non trovata"})

    serializer = BookingSerializer(booking, request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message":"prenotazione aggiornata con successo"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

