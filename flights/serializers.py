
from .models import Agent, Airline, Airport, Leg, Itinerary
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """Abstract serializer to be used as base when possible."""

    id = serializers.SerializerMethodField('get_prefixed_id')
    id_prefix: str = ''

    class Meta():
        abstract = True
        exclude = ('created_at', 'updated_at')

    def get_prefixed_id(self, obj) -> str:
        """ Example:
            If the prefix passed in the meta class is 'leg' and id is 1. Returns 'leg_1'"""

        prefix = self.id_prefix
        return f'{prefix}_{obj.id}' if prefix else obj.id


class AirlinesSerializer(BaseSerializer):
    id_prefix = 'al'

    class Meta(BaseSerializer.Meta):
        model = Airline


class AirportsSerializer(BaseSerializer):
    id_prefix = 'ap'

    class Meta(BaseSerializer.Meta):
        model = Airport


class AgentSerializer(BaseSerializer):
    id_prefix = 'ag'

    class Meta(BaseSerializer.Meta):
        model = Agent


class LegSerializer(BaseSerializer):
    id_prefix = 'leg'

    departure_airport = AirportsSerializer()
    arrival_airport = AirportsSerializer()
    airline = AirlinesSerializer()

    class Meta(BaseSerializer.Meta):
        model = Leg


class ItinerarySerializer(BaseSerializer):
    legs = LegSerializer(many=True)
    agent = AgentSerializer()
    pricing = serializers.SerializerMethodField('get_pricing')

    class Meta(BaseSerializer.Meta):
        model = Itinerary
        prefix = 'it'

    def get_pricing(self, obj) -> str:
        return f'{obj.pricing.currency}{obj.pricing.price}'
