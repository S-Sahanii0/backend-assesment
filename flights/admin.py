from django.contrib import admin
from .models import Airline, Airport, Itinerary, Leg, Agent, Pricing


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
admin.site.register(Agent)
admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Pricing)
