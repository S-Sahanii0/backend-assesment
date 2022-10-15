

from rest_framework import serializers
from .models import Agent, Airline, Airport, Leg, Itinerary


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_prefixed_id')

    class Meta:
        abstract = True
        prefix = None
        exclude = ('created_at', 'updated_at')

    def get_prefixed_id(self, obj):
        prefix = self.Meta.prefix
        return f'{prefix}_{obj.id}' if prefix else obj.id


class AirlinesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Airline
        prefix = 'al'


class AirportsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Airport
        prefix = 'ap'


class AgentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Agent
        prefix = 'ag'


class LegSerializer(BaseSerializer):
    departure_airport = AirportsSerializer()
    arrival_airport = AirportsSerializer()
    airline = AirlinesSerializer()

    class Meta(BaseSerializer.Meta):
        model = Leg
        prefix = 'leg'


class ItinerarySerializer(BaseSerializer):
    legs = LegSerializer(many=True)
    agent = AgentSerializer()
    pricing = serializers.SerializerMethodField('get_pricing')

    class Meta(BaseSerializer.Meta):
        model = Itinerary
        prefix = 'it'

    def get_pricing(self, obj):
        return f'{obj.pricing.currency}{obj.pricing.price}'
