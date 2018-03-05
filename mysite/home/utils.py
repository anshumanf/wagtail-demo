from django.core.urlresolvers import reverse

from wagtail.wagtailcore.models import Site


def generate_image_url(image, filter_spec):
    from wagtail.wagtailimages.views.serve import generate_signature
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    try:
        site_root_url = Site.objects.get(is_default_site=True).root_url
    except Site.DoesNotExist:
        site_root_url = Site.objects.first().root_url

    image_filename = image.file.name[len('original_images/'):]

    return site_root_url + url + image_filename
