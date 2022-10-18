from typing import Collection

from celery import shared_task
from flights.utils import split_currency_and_amount, make_request
from flights.models import Agent, Airline, Airport, Itinerary, Leg, Pricing
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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

    logger.info('Importing legs...')
    existing_legs_id_list: Collection[int] = Leg.objects.all(
    ).values_list('id', flat=True)

    for leg in fresh_legs:
        prefixed_leg_id = leg.pop('id')
        unprefixed_leg_id = prefixed_leg_id.lstrip('leg_')
        if unprefixed_leg_id not in existing_legs_id_list:
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
            Leg.objects.get_or_create(id =unprefixed_leg_id,
                airline=airline, arrival_airport=arrival_airport, departure_airport=departure_airport, **leg)


def import_itineraries(fresh_itineraries: list[dict]):
    """Imports itineraries which are not already in the database."""
    
    logger.info('Importing itineraries...')

    existing_itineraries_id_list: Collection[int] = Leg.objects.all(
    ).values_list('id', flat=True)
    
    for itinerary in fresh_itineraries:
        prefixed_it_id = itinerary.pop('id')
        unprefixed_it_id = prefixed_it_id.lstrip('it_')
        if unprefixed_it_id not in existing_itineraries_id_list:
    
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
                id__in=[prefixed_leg_id.lstrip('leg_') for prefixed_leg_id in itinerary.pop('legs')])

            itineraries, _ = Itinerary.objects.get_or_create(id = unprefixed_it_id,
                pricing=pricing, agent=agent, **itinerary)
            itineraries.legs.add(legs)
