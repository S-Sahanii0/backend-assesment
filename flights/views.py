from rest_framework import generics
from flights.serializers import ItinerarySerializer
from .models import Itinerary
from rest_framework import filters
from drf_yasg.inspectors import SwaggerAutoSchema


class ItineraryListView(generics.ListAPIView):
    queryset = Itinerary.objects.all()
    swagger_schema = SwaggerAutoSchema
    serializer_class = ItinerarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['agent__name']
    ordering_fields = ['pricing__price']
