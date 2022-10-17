from django.contrib import admin
from .models import Airline, Airport, Itinerary, Leg, Agent, Pricing
from django_object_actions import DjangoObjectActions


class AgentAdmin(admin.ModelAdmin):
    list_display: list[str] = ['name', 'rating']
    search_fields: list[str] = ['name']
    
class AirlineAdmin(admin.ModelAdmin):
    list_display: list[str] = ['name', 'code']
    search_fields: list[str] = ['name', 'code']
    
class AirportAdmin(admin.ModelAdmin):
    search_fields: list[str] = ['name']
    

    
class LegsInline(admin.TabularInline):
    verbose_name = 'Leg'
    model = Itinerary.legs.through


class LegInline(admin.ModelAdmin):
    inlines = [LegsInline]
    list_display: list[str] = ['departure_airport', 'arrival_airport', 'airline', 'departure_time', 'arrival_time']
    search_fields: list[str] = ['airline__name', 'airline__code', 'departure_airport__name', 'arrival_airport__name']


class ItineraryAdmin(DjangoObjectActions, admin.ModelAdmin):
    inlines = [LegsInline]
    list_display: list[str] = ['agent', 'pricing']
    exclude = ['legs']
    search_fields: list[str] = ['id', 'agent__name']
    ordering: list[str] = ['pricing__price']
    changelist_actions = ['import_data']
    
    def import_data(self, request, obj):
        print('import_data')
        
    
        
    
    


admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Leg, LegInline)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Airport, AirportAdmin)
