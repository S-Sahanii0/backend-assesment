from email.policy import default
from django.db import models


class Itinerary(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default='it_000')
    legs = models.ManyToManyField('Leg', related_name='leg')
    price = models.CharField(max_length=10)
    agent = models.CharField(max_length=100)
    agent_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.id


class Leg(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default='leg_000')
    departure_airport = models.CharField(max_length=3)
    arrival_airport = models.CharField(max_length=3)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    stops = models.IntegerField()
    airline_name = models.CharField(max_length=100)
    airline_id = models.CharField(max_length=2)
    duration_mins = models.IntegerField()

    def __str__(self):
        return self.departure_airport + " to " + self.arrival_airport
