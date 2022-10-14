# Generated by Django 4.1.2 on 2022-10-13 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('price', models.CharField(max_length=10)),
                ('agent', models.CharField(max_length=100)),
                ('agent_rating', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Leg',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('departure_airport', models.CharField(max_length=3)),
                ('arrival_airport', models.CharField(max_length=3)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('stops', models.IntegerField()),
                ('airline_name', models.CharField(max_length=100)),
                ('airline_id', models.CharField(max_length=2)),
                ('duration_mins', models.IntegerField()),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary', to='flights.itinerary')),
            ],
        ),
    ]
