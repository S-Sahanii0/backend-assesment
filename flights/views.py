from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from config.settings import CACHE_TTL
from flights.ordering import PriceOrderingFilter
from flights.serializers import ItinerarySerializer
from .models import Itinerary
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ItineraryListView(generics.ListAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    filter_backends = [filters.SearchFilter, PriceOrderingFilter]
    search_fields = ['agent__name']

    @swagger_auto_schema(
        operation_description="""Get All Itineraries.
        
        Search fields = Agent Name
        Ordering fields = [highest_price, lowest_price]
        """,
        responses={200: ItinerarySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
