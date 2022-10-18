from rest_framework import generics, pagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from config.settings import CACHE_TTL
from flights.filters import PriceOrderingFilter, FlightsFilter
from flights.serializers import ItinerarySerializer
from .models import Itinerary, Leg
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from django.db.models.query import Prefetch
from drf_yasg import openapi




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ItineraryListView(generics.ListAPIView):
    """List all itineraries."""
    
    queryset = Itinerary.objects.prefetch_related(
        Prefetch(
            'legs',
            queryset = Leg.objects.
            select_related('departure_airport', 'arrival_airport', 'airline').all()
        )
        ).select_related('agent').all()
    serializer_class = ItinerarySerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [PriceOrderingFilter, FlightsFilter]

    @swagger_auto_schema(
        operation_description="""Get All Itineraries.
        
        Search fields: [stops, airline, agent]
        Ordering fields: [Price(highest_price, lowest_price) OR Rating(highest_rating, lowest_rating)]
        """,
        responses={200: ItinerarySerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('stops', openapi.IN_QUERY, 
                              description="Filter by number of stops.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('agent', openapi.IN_QUERY, 
                              description="Filter by agent name.", type=openapi.TYPE_STRING),
            openapi.Parameter('airline', openapi.IN_QUERY, 
                              description="Filter by airlines.", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
