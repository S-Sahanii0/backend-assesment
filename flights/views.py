from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from config.settings import CACHE_TTL
from flights.ordering import PriceOrderingFilter
from flights.serializers import ItinerarySerializer
from .models import Itinerary
from rest_framework import filters
from drf_yasg.inspectors import SwaggerAutoSchema


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ItineraryListView(generics.ListAPIView):
    queryset = Itinerary.objects.all()
    swagger_schema = SwaggerAutoSchema
    serializer_class = ItinerarySerializer
    filter_backends = [filters.SearchFilter, PriceOrderingFilter]
    search_fields = ['agent__name']
