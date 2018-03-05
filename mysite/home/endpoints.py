from wagtail.api.v2.endpoints import BaseAPIEndpoint, PagesAPIEndpoint

from wagtail.api.v2.filters import (FieldsFilter, OrderingFilter, SearchFilter)

from wagtail.api.v2.utils import BadRequestError

from rest_framework.renderers import BrowsableAPIRenderer

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from .serializers import SimulationExampleSerializer
from .models import SimulationExample


class WebsimPagesAPIEndpoint(PagesAPIEndpoint):
    renderer_classes = [CamelCaseJSONRenderer, BrowsableAPIRenderer]


class SimulationExamplesAPIEndpoint(BaseAPIEndpoint):
    renderer_classes = [CamelCaseJSONRenderer, BrowsableAPIRenderer]

    base_serializer_class = SimulationExampleSerializer

    filter_backends = [
        FieldsFilter,
        OrderingFilter,
        SearchFilter
    ]
    known_query_parameters = BaseAPIEndpoint.known_query_parameters.union([
    ])
    body_fields = [
        'id',
    ]
    meta_fields = [
    ]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + [
        'id',
        'name',
    ]
    nested_default_fields = BaseAPIEndpoint.nested_default_fields + [
        'id',
        'name',
    ]
    detail_only_fields = [
        'code',
        'language',
        'universe',
    ]
    name = 'simulationexamples'
    model = SimulationExample

    def get_queryset(self):
        models = None

        if not models:
            models = [SimulationExample]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = SimulationExample.objects.all()

        return queryset

    def get_object(self):
        base = super(SimulationExamplesAPIEndpoint, self).get_object()
        return base

    def check_query_parameters(self, queryset):
        """
        Ensure that only valid query paramters are included in the URL.
        """
        query_parameters = set(self.request.GET.keys())

        # All query paramters must be either a database field or an operation
        allowed_query_parameters = set(self.get_available_fields(queryset.model, db_fields_only=True)).union(self.known_query_parameters)

        print str(set(self.get_available_fields(queryset.model, db_fields_only=True)))

        unknown_parameters = query_parameters - allowed_query_parameters
        if unknown_parameters:
            raise BadRequestError("query parameter is not an operation or a recognised field: %s" % ', '.join(sorted(unknown_parameters)))

    @classmethod
    def _get_serializer_class(cls, router, model, fields_config, show_details=False, nested=False):
        # Get all available fields
        body_fields = cls.get_body_fields_names(model)
        meta_fields = cls.get_meta_fields_names(model)
        all_fields = body_fields + meta_fields
        from collections import OrderedDict
        # Remove any duplicates
        all_fields = list(OrderedDict.fromkeys(all_fields))

        print 'body_fields ' + str(body_fields)
        print 'meta_fields ' + str(meta_fields)
        print 'all_fields ' + str(all_fields)

        if not show_details:
            # Remove detail only fields
            for field in cls.detail_only_fields:
                try:
                    all_fields.remove(field)
                except KeyError:
                    pass

        # Get list of configured fields
        if show_details:
            fields = set(cls.get_detail_default_fields(model))
        elif nested:
            fields = set(cls.get_nested_default_fields(model))
        else:
            fields = set(cls.get_listing_default_fields(model))

        print 'fields_config : ' + str(fields_config)

        # If first field is '*' start with all fields
        # If first field is '_' start with no fields
        if fields_config and fields_config[0][0] == '*':
            fields = set(all_fields)
            fields_config = fields_config[1:]
        elif fields_config and fields_config[0][0] == '_':
            fields = set()
            fields_config = fields_config[1:]

        mentioned_fields = set()
        sub_fields = {}

        for field_name, negated, field_sub_fields in fields_config:
            if negated:
                try:
                    fields.remove(field_name)
                except KeyError:
                    pass
            else:
                fields.add(field_name)
                if field_sub_fields:
                    sub_fields[field_name] = field_sub_fields

            mentioned_fields.add(field_name)

        unknown_fields = mentioned_fields - set(all_fields)

        if unknown_fields:
            raise BadRequestError("unknown fields: %s" % ', '.join(sorted(unknown_fields)))

        print 'fields : ' + str(fields)

        # Build nested serialisers
        child_serializer_classes = {}
        from django.core.exceptions import FieldDoesNotExist
        for field_name in fields:
            try:
                django_field = model._meta.get_field(field_name)
            except FieldDoesNotExist:
                django_field = None

            if django_field and django_field.is_relation:
                child_sub_fields = sub_fields.get(field_name, [])
                from modelcluster.fields import ParentalKey
                # Inline (aka "child") models should display all fields by default
                if isinstance(getattr(django_field, 'field', None), ParentalKey):
                    if not child_sub_fields or child_sub_fields[0][0] not in ['*', '_']:
                        child_sub_fields = list(child_sub_fields)
                        child_sub_fields.insert(0, ('*', False, None))

                # Get a serializer class for the related object
                child_model = django_field.related_model
                child_endpoint_class = router.get_model_endpoint(child_model)
                child_endpoint_class = child_endpoint_class[1] if child_endpoint_class else BaseAPIEndpoint
                child_serializer_classes[field_name] = child_endpoint_class._get_serializer_class(router, child_model, child_sub_fields, nested=True)

            else:
                if field_name in sub_fields:
                    # Sub fields were given for a non-related field
                    raise BadRequestError("'%s' does not support nested fields" % field_name)

        # Reorder fields so it matches the order of all_fields
        fields = [field for field in all_fields if field in fields]

        field_serializer_overrides = {field[0]: field[1] for field in cls.get_field_serializer_overrides(model).items() if field[0] in fields}
        from wagtail.api.v2.serializers import get_serializer_class
        return get_serializer_class(
            model,
            fields,
            meta_fields=meta_fields,
            field_serializer_overrides=field_serializer_overrides,
            child_serializer_classes=child_serializer_classes,
            base=cls.base_serializer_class
        )
