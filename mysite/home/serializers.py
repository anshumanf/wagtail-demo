from django.forms.models import model_to_dict

from rest_framework import serializers

from .utils import generate_image_url


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, image):
        fields = [
            'title',
            'width',
            'height',
            'file_size',
        ]
        retVal = {}

        for field in fields:
            retVal[field] = getattr(image, field)

        if self.context is not None and getattr(self.context, 'width', None) is not None:
            image_width_spec = 'width-' + str(self.context.width)
        else:
            image_width_spec = 'original'

        retVal['url'] = generate_image_url(image, image_width_spec)

        return retVal


class CodeSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, code):
        print str(code)
        return code


class SimulationExampleSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, simulation):
        model_dict = model_to_dict(simulation)
        return {k: model_dict[k] for k in self.fields}
