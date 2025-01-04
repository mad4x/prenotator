from .models import Booking

def checkOverlappingBookings(serializer):
    booking_data = serializer.validated_data
    overlapping_bookings = Booking.objects.filter(
        lab = booking_data['lab'],
        date = booking_data['date'],
        start_time__lt = booking_data['end_time'],
        end_time__gt = booking_data['start_time']
    )
    if overlapping_bookings.exists():
        return True

    return False
