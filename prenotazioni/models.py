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
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.name} ha prenotato {self.lab}\n"
                f"{self.date.strftime('%d/%m/%Y')}   {self.start_time.strftime('%H:%M')} - {self.start_time.strftime('%H:%M')}")
