from typing import Collection

from celery import shared_task
from flights.utils import split_currency_and_amount, make_request
from flights.models import Agent, Airline, Airport, Itinerary, Leg, Pricing


@shared_task()
def import_external_data():
    """Fetches legs and itineraries from the source url 
    and has a side-effect of storing them into the database."""

    response = make_request(
        'https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json')

    import_legs(response['legs'])
    import_itineraries(response['itineraries'])


def import_legs(fresh_legs: list[dict]):
    """Imports legs which are not already in the database."""

    existing_legs_id_list: Collection[int] = Leg.objects.all(
    ).values_list('id', flat=True)

    for leg in fresh_legs:
        if leg.pop('id').lstrip('leg_') not in existing_legs_id_list:
            airline, _ = Airline.objects.get_or_create(**{
                'name': leg.pop('airline_name'),
                'code': leg.pop('airline_id')
            })
            arrival_airport, _ = Airport.objects.get_or_create(**{
                'name': leg.pop('arrival_airport')
            })
            departure_airport, _ = Airport.objects.get_or_create(**{
                'name': leg.pop('departure_airport')
            })
            Leg.objects.get_or_create(
                airline=airline, arrival_airport=arrival_airport, departure_airport=departure_airport, **leg)


def import_itineraries(fresh_itineraries: list[dict]):
    """Imports itineraries which are not already in the database."""

    existing_itineraries_id_list: Collection[int] = Leg.objects.all(
    ).values_list('id', flat=True)

    for itinerary in fresh_itineraries:
        if itinerary.pop('id').lstrip('it_') not in existing_itineraries_id_list:
            currency, price = split_currency_and_amount(itinerary.pop('price'))
            pricing, _ = Pricing.objects.get_or_create(**{
                'currency':  currency,
                'price': price,
            })
            agent, _ = Agent.objects.get_or_create(**{
                'name': itinerary.pop('agent'),
                'rating': itinerary.pop('agent_rating')
            })
            legs, _ = Leg.objects.filter(
                id__in=[leg.lstrip('leg_') for leg in itinerary.pop('legs')])

            itineraries, _ = Itinerary.objects.get_or_create(
                pricing=pricing, agent=agent, **itinerary)
            itineraries.legs.add(legs)
