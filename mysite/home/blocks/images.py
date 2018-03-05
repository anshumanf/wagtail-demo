from wagtail.wagtailimages.blocks import ImageChooserBlock

from home.serializers import ImageSerializer


class APIImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return ImageSerializer(context=context).to_representation(value)
