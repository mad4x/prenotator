from rest_framework import serializers
from .models import Booking
from django.utils import timezone

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_start_time(self, value):
        if value is None:
            serializers.ValidationError("L'orario d'inizio è obbligatorio.")
        if value < timezone.now():
            serializers.ValidationError("Non puoi effettuare una prenotazione nel passato.")
        return value

