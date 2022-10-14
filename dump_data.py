import requests
from flights.models import *

data_url = 'https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json'


def main():
    """Imports data from a URL in the itinerary database."""

    data: dict = requests.get(data_url).json()
    itineraries: list[dict] = data['itineraries']
    legs: list[dict] = data['legs']

    for itinerary in itineraries:
        try:
            list_of_legs = itinerary.pop('legs')
            new_itinerary = Itinerary.objects.create(**itinerary)
            for leg_id in list_of_legs:
                try:
                    leg = Leg.objects.get(id=leg_id)
                except Leg.DoesNotExist:
                    leg = Leg.objects.create(
                        **[leg for leg in legs if leg['id'] == leg_id][0])
                new_itinerary.legs.add(
                    leg
                )
            new_itinerary.save()

        except Exception as e:
            print(e)


main()
