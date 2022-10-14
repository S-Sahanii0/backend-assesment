from typing import Sequence
from django.contrib import admin
from .models import Itinerary, Leg


class LegsInline(admin.TabularInline):
    verbose_name = 'Leg'
    model = Itinerary.legs.through


class LegInline(admin.ModelAdmin):
    inlines = [LegsInline]


class ItineraryAdmin(admin.ModelAdmin):
    inlines = [LegsInline]
    exclude = ['legs']


admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Leg, LegInline)
