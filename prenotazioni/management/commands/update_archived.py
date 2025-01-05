import pytz
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from prenotazioni.models import Booking

class Command(BaseCommand):
    help = "Aggiorna lo stato 'is_archived' delle prenotazioni scadute"

    def handle(self, *args, **kwargs):
        local_tz = pytz.timezone('Europe/Rome')
        now = timezone.now().astimezone(local_tz)
        expired_bookings = Booking.objects.filter(
            Q(date__lt = now.date(), is_archived = False) |
            Q(date = now.date(), start_time__lt = now.time(), is_archived = False)
        )
        count = expired_bookings.update(is_archived=True)
        self.stdout.write(f"{count} prenotazioni archiviate.")
