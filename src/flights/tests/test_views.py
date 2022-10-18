
import json
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework.response import Response

from flights.models import Itinerary



class ItineraryViewTest(APITestCase):
    
    def test_list_itineraries(self):
        """
        Ensure list of itineraries is correctly returned.
        """
        response = self.client.get('/flights/itineraries/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_itineraries_with_search(self):
        """
        Given a search parameter q, returns a list of data containing that parameter.
        If not returns an empty list.
        """
        
        itinerary = baker.make(Itinerary, agent__name="Test") 
        response = self.client.get('/flights/itineraries/?search=Test',{'search': 'Test'}, format='json')
        
        data = response.json()
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['id'], f'it_{itinerary.pk}')

        
    def test_list_itineraries_with_ordering(self):
        """
        Ensure list of itineraries is correctly returned with price ordering.
        """
        
        baker.make(Itinerary, pricing__price = 100)
        baker.make(Itinerary, pricing__price = 200)
        
        response = self.client.get('/flights/itineraries/?search=Test',{'ordering': 'highest_price'}, format='json')
        
        data = response.content.decode('utf-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(data)[0]['pricing'] > json.loads(data)[1]['pricing'] , True)
        