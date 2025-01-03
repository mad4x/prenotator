from datetime import datetime, timedelta
import pytz
from rest_framework import serializers
from .models import Booking
from django.utils import timezone

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_date(self, value):
        if value < timezone.now().date():  #errore: data passata
            raise serializers.ValidationError("Non puoi effettuare una prenotazione nel passato.")
        return value

    def validate(self, data):
        local_tz = pytz.timezone('Europe/Rome')
        current_time = timezone.now().astimezone(local_tz).time()
        current_date = timezone.now().astimezone(local_tz).date()
        #prende i dati dalla richiesta se sono presenti, altrimenti dall'istanza da aggiornare
        if 'date' in self.initial_data:
            date = data.get('date')
        else:
            date = self.instance.date

        if 'start_time' in self.initial_data:
            start_time = data.get('start_time')
        else:
            start_time = self.instance.start_time

        if 'end_time' in self.initial_data:
            end_time = data.get('end_time')
        else:
            end_time = self.instance.end_time

        #se la prenotazione è ad un orario già passato
        if date == timezone.now().date() and start_time < current_time:
                raise serializers.ValidationError("Non puoi effettuare una prenotazione nel passato.")
        #se l'ora di fine e prima di quella d'inizio
        if end_time < start_time:
            raise serializers.ValidationError("L'orario di fine non può essere prima di quello d'inizio.")
        #se la prenotazione dura più di 2 ore
        start_datatime = datetime.combine(datetime.today(), start_time)
        end_datatime = datetime.combine(datetime.today(), end_time)
        if end_datatime - start_datatime > timedelta(hours=2):
            raise serializers.ValidationError("La prenotazione deve essere meno lunga di 2 ore.")
        #se la prenotazione viene effettuata più di 30 giorni prima
        if date - current_date > timedelta(days=30):
            raise serializers.ValidationError("La prenotazione non può essere effettuata più di 30 giorni prima.")

        return data