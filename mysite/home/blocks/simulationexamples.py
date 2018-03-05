from django import forms

from wagtail.wagtailcore import blocks

from home.serializers import SimulationExampleSerializer
from home.models.simulationexamples import SimulationExample


class SimulationExampleChooserBlock(blocks.ChooserBlock):
    target_model = SimulationExample
    widget = forms.Select

    class Meta:
        icon = 'code'

    def get_api_representation(self, value, context=None):
        return SimulationExampleSerializer(context=context).to_representation(value)

    def render(self, value, **kwargs):
        kwargs.pop('context', None)
        return '\
        <pre>Language : ' + value.language + '</pre>' + '\
        <pre>Universe : ' + value.universe + '</pre>' + '\
        <code>' + value.code + '</code>'
