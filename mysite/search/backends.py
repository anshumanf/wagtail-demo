from wagtail.wagtailsearch.backends.elasticsearch.py import (
  ElasticsearchSearchQuery,
  ElasticsearchSearchResults,
  ElasticsearchSearchBackend,
)

from wagtail.wagtailsearch.backends.elasticsearch2.py import (
  Elasticsearch2SearchQuery,
  Elasticsearch2SearchBackend,
)

from wagtail.wagtailsearch.backends.elasticsearch.py import (
  Elasticsearch5SearchQuery,
  Elasticsearch5SearchBackend,
)


class ElasticsearchSearchHighlightingResults(ElasticsearchSearchResults):
    def _get_es_body(self, for_count=False):
        body = {
            'query': self.query.get_query(),
            'highlight': {
                'fields' : {
                    'title': {},
                    'home_article__title_es': {},
                    'home_article__body_en': {},
                    'home_article__body_es': {}
                }
              },
        }

        if not for_count:
            sort = self.query.get_sort()

            if sort is not None:
                body['sort'] = sort

        return body

    def _do_search(self):
        # Params for elasticsearch query
        params = dict(
            index=self.backend.get_index_for_model(self.query.queryset.model).name,
            body=self._get_es_body(),
            _source=False,
            from_=self.start,
        )

        params[self.fields_param_name] = 'pk'

        # Add size if set
        if self.stop is not None:
            params['size'] = self.stop - self.start

        # Send to Elasticsearch
        hits = self.backend.es.search(**params)

        print 'Hits : ' + str(hits)

        # Get pks from results
        pks = [hit['fields']['pk'][0] for hit in hits['hits']['hits']]
        scores = {str(hit['fields']['pk'][0]): hit['_score'] for hit in hits['hits']['hits']}

        # Initialise results dictionary
        results = dict((str(pk), None) for pk in pks)

        # Find objects in database and add them to dict
        queryset = self.query.queryset.filter(pk__in=pks)
        for obj in queryset:
            results[str(obj.pk)] = obj

            if self._score_field:
                setattr(obj, self._score_field, scores.get(str(obj.pk)))

        # Return results in order given by Elasticsearch
        return [results[str(pk)] for pk in pks if results[str(pk)]]


class ElasticsearchSearchHighlightingBackend(ElasticsearchSearchBackend):
    query_class = ElasticsearchSearchQuery
    results_class = ElasticsearchSearchResults


class Elasticsearch2SearchHighlightingResults(ElasticsearchSearchHighlightingResults):
    pass


class Elasticsearch2SearchHighlightingBackend(Elasticsearch2SearchBackend):
    query_class = Elasticsearch2SearchQuery
    results_class = Elasticsearch2SearchHighlightingResults


class Elasticsearch5SearchHighlightingResults(Elasticsearch2SearchHighlightingResults):
    pass


class Elasticsearch5SearchHighlightingBackend(Elasticsearch5SearchBackend):
    query_class = Elasticsearch5SearchQuery
    results_class = Elasticsearch5SearchHighlightingResults


SearchBackend = Elasticsearch5SearchHighlightingBackend
