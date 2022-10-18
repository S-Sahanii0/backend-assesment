
import json
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework.response import Response

from flights.models import Itinerary
from flights.serializers import ItinerarySerializer



class ItineraryListViewTest(APITestCase):
    
    def test_list_itineraries(self):
        """
        Ensure list of itineraries is correctly returned.
        """
        
        response = self.client.get('/flights/itineraries/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_itineraries_with_filtering(self):
        """
        Given a parameter q, returns a list of data containing that parameter.
        If not returns an empty list.
        """
        
        itinerary = baker.make(Itinerary, agent__name="Test") 
        itinerary2 = baker.make(Itinerary, agent__name="Test1")
        response = self.client.get('/flights/itineraries/',{'agent': 'Test'}, format='json')
        
        data = response.json()['results']
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['id'], f'it_{itinerary.pk}')

        
    def test_list_itineraries_with_ordering(self):
        """
        Ensure list of itineraries is correctly returned with price ordering.
        """
        
        baker.make(Itinerary, pricing__price = 100)
        baker.make(Itinerary, pricing__price = 200)
        
        response = self.client.get('/flights/itineraries/?search=Test',{'ordering': 'highest_price'}, format='json')
        
        data = response.json()['results']
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((data)[0]['pricing'] > (data)[1]['pricing'] , True)
        