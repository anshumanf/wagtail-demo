from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from wagtail.api import APIField

from rest_framework import serializers

from .translation import TranslatedField


class HomePage(Page):
    title_es = models.CharField(blank=True, max_length=255)

    body_en = RichTextField(blank=True)
    body_es = RichTextField(blank=True)

    translated_title = TranslatedField(
        'title',
        'title_es',
    )

    body = TranslatedField(
        'body_en',
        'body_es',
    )

    content_en_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body_en', classname="full"),
    ]
    content_es_panels = [
        FieldPanel('title_es', classname="full title"),
        FieldPanel('body_es', classname="full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_en_panels, heading='Content (EN)'),
        ObjectList(content_es_panels, heading='Content (ES)'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    api_fields = [
        APIField('title', serializers.CharField(source='translated_title')),
        APIField('body', serializers.CharField()),
    ]
