from django.urls import path

from unicodedata import name

from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('itineraries/', views.ItineraryListView.as_view(), name='itinerary-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
