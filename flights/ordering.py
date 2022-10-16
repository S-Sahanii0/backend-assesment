from rest_framework.filters import OrderingFilter


class PriceOrdering(OrderingFilter):
    """Custom ordering filter for price field of the itinerary.
    It allows to order by [highest_price] or [lowest_price].
    """

    allowed_custom_filters = ['highest_price', 'lowest_price']
    fields_related = {  # Lookup for the related field of the price
        'highest_price': '-pricing__price',
        'lowest_price': 'pricing__price'
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
