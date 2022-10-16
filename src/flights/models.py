from datetime import datetime
from email.policy import default
from enum import unique
from locale import currency
import ssl
from sys import prefix
from tabnanny import verbose
from django.db import models


class BaseModel(models.Model):
    """Abstract model to be used as base when possible."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    # @property  # type: ignore
    # def prefixed_id(self, prefix):
    #     return f'{prefix}_{id}'


class Airline(BaseModel):
    """Model representing an airline."""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    # agent = models.OneToOneField('Agent', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.code}'


class Airport(BaseModel):
    """Model representing an Airport."""

    name = models.CharField(max_length=100)
    # city = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Agent(BaseModel):
    """Model representing a travel agent."""

    name = models.CharField(max_length=100)
    rating = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Pricing(BaseModel):
    """Model representing the currency and amount."""

    currency = models.CharField(max_length=1, default='£')
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.currency} {self.price}'


class Leg(BaseModel):
    """Model representing journeys (outbound, return) 
    with duration, stops and airlines"""

    departure_airport = models.ForeignKey(
        Airport,  on_delete=models.CASCADE, related_name='departure_airport')
    arrival_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='arrival_airport')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    stops = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    duration_mins = models.IntegerField()

    def __str__(self):
        return f'{self.departure_airport} - {self.arrival_airport}'


class Itinerary(BaseModel):
    """Model representing trips, tying together legs, and prices"""

    legs = models.ManyToManyField(Leg)
    pricing = models.OneToOneField(Pricing, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.agent} - {self.pricing}'
