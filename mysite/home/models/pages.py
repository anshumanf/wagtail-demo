from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList

from wagtail.api import APIField
from wagtail.api.v2 import serializers as wagtail_serializers

from rest_framework import serializers

from wagtail.wagtailsearch import index

from home.blocks.images import APIImageChooserBlock
from home.blocks.simulationexamples import SimulationExampleChooserBlock
from home.translation import TranslatedField


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
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    api_fields = [
        APIField('title', serializers.CharField(source='translated_title')),
        APIField('body', serializers.CharField()),
    ]


class Article(Page):
    template = 'home/article.html'

    title_es = models.CharField(blank=True, max_length=255)

    body_en = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('example', SimulationExampleChooserBlock()),
        ('image', APIImageChooserBlock()),
        ('table', TableBlock()),
    ])
    body_es = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('example', SimulationExampleChooserBlock()),
        ('image', APIImageChooserBlock()),
        ('table', TableBlock()),
    ])

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
        StreamFieldPanel('body_en', classname="full"),
    ]
    content_es_panels = [
        FieldPanel('title_es', classname="full title"),
        StreamFieldPanel('body_es', classname="full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_en_panels, heading='Content (EN)'),
        ObjectList(content_es_panels, heading='Content (ES)'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    api_fields = [
        APIField('title', serializers.CharField(source='translated_title')),
        APIField('body', wagtail_serializers.StreamField()),
    ]

    search_fields = [
        index.FilterField('live'),
        index.FilterField('path'),
        index.FilterField('depth'),
        index.SearchField('title', partial_match=True, boost=2),
        index.SearchField('title_es', partial_match=True, boost=2),
        index.SearchField('body_en', partial_match=True),
        index.SearchField('body_es', partial_match=True),
    ]
