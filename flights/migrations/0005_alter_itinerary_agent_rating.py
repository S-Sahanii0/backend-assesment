# Generated by Django 4.1.2 on 2022-10-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_remove_leg_itinerary_itinerary_legs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='agent_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
