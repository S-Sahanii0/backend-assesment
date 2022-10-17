from tracemalloc import BaseFilter
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend

class FlightsFilter(BaseFilterBackend):
    """
    Custom filter to filter by stops, airlines name and agents name.
    """
    
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('stops'):
            queryset = queryset.filter(legs__stops=request.query_params.get('stops'))
        if request.query_params.get('airline'):
            queryset = queryset.filter(legs__airline__name=request.query_params.get('airline'))
        if request.query_params.get('agent'):
            queryset = queryset.filter(agent__name=request.query_params.get('agent'))
        return queryset
    
class PriceOrderingFilter(OrderingFilter):
    """Custom ordering filter for price field of the itinerary.
    It allows to order by [Pricing] or [Rating].
    """

    allowed_custom_filters = ['highest_price', 'lowest_price', 'highest_rating', 'lowest_rating' ]
    fields_related = {  # Lookup for the related field of the price
        'highest_price': '-pricing__price',
        'lowest_price': 'pricing__price',
        'highest_rating': '-agent__rating',
        'lowest_rating': 'agent__rating',
    
    }

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = [f for f in fields if f in self.allowed_custom_filters]
            if ordering:
                return ordering

        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        order_fields = []
        ordering = self.get_ordering(request, queryset, view)
        print(ordering)
        if ordering:
            for field in ordering:
                order_fields.append(
                    self.fields_related[field])
        if order_fields:
            return queryset.order_by(*order_fields)

        return queryset
