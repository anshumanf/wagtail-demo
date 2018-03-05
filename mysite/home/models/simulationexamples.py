from django.db import models

from wagtail.api import APIField
from wagtail.wagtailsearch import index

from rest_framework import serializers


class BaseSimulation(index.Indexed, models.Model):
    UNIVERSE_CHOICES = (
        ('TOP3000', 'TOP3000'),
        ('TOP2000', 'TOP2000'),
    )

    LANGUAGE_CHOICES = (
        ('EXPRESSION', 'Expression'),
        ('PYTHON', 'Python'),
    )

    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10)
    code = models.TextField()
    universe = models.CharField(choices=UNIVERSE_CHOICES, max_length=10)

    api_fields = [
        APIField('language', serializers.CharField()),
        APIField('code', serializers.CharField()),
        APIField('universe', serializers.CharField()),
    ]

    search_fields = [
        index.SearchField('language'),
        index.SearchField('code', partial_match=True),
        index.SearchField('universe'),
    ]

    class Meta:
        abstract = True


class SimulationExample(BaseSimulation):
    name = models.CharField(max_length=100)

    api_fields = [
        APIField('name', serializers.CharField()),
    ] + BaseSimulation.api_fields

    search_fields = [
        index.SearchField('name'),
    ] + BaseSimulation.search_fields

    def __str__(self):
        return self.name
