from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from rest_framework.response import Response


class Booking(models.Model):
    LAB_CHOICES = [
        ('LAB1', 'Laboratorio 1'),
        ('LAB2', 'Laboratorio 2')
    ]
    lab = models.CharField(max_length=15, choices=LAB_CHOICES)
    name = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.date < now() or self.start_time < now():
            raise ValidationError("Non si può effettuare una prenotazione nel passato.")
        elif self.end_time < self.start_time:
            raise ValidationError("La orario di fine deve venire dopo di quello d'inizio.")


    def __str__(self):
        return (f"{self.name} ha prenotato {self.lab}\n"
                f"{self.date.strftime('%d/%m/%Y')}   {self.start_time.strftime('%H:%M')} - {self.start_time.strftime('%H:%M')}")
