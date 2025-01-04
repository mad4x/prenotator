import pytz
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from prenotazioni.models import Booking
from prenotazioni.serializers import BookingSerializer
from .utils import checkOverlappingBookings

local_tz = pytz.timezone('Europe/Rome')

@api_view(['GET'])
def listBookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listActiveBookings(request):
    bookings = Booking.objects.filter(is_archived=False)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listArchivedBookings(request):
    bookings = Booking.objects.filter(is_archived=True)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listBookingsByName(request, name):
    bookings = Booking.objects.filter(name=name)
    serializer = BookingSerializer(bookings, many=True)
    if not bookings.exists():
        return Response({"message":"non ci sono prenotazioni a questo nome"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)

@api_view(['GET'])
def listBookingsByDate(request, date):
    bookings = Booking.objects.filter(date=date)
    serializer = BookingSerializer(bookings, many=True)
    if not bookings.exists():
        return Response({"message":"non ci sono prenotazioni a questa data"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(['POST'])
def addBooking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        #controllo sovrappozioni
        if checkOverlappingBookings(serializer):
            return Response({"unavailable":"laboratorio non disponibile all'orario selezionato"},
                            status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBooking(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"error":"prenotazione non trovata"},
                        status=status.HTTP_404_NOT_FOUND)
    #se la prenotazione è passata
    if booking.is_archived:
        return Response({"error":"impossibile cancellare prenotazioni passate"})

    booking.delete()
    return Response({"message":"prenotazione eliminata con successo"},
                    status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
def updateBooking(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"error":"prenotazione non trovata"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = BookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        # controllo sovrappozioni
        if checkOverlappingBookings(serializer):
            return Response({"unavailable": "laboratorio non disponibile all'orario selezionato"},
                            status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response({"message":"prenotazione aggiornata con successo"},
                        status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

