from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.wagtailsearch.models import Query

from home.models import Article


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Article.objects.live().search(search_query)
        print len(Article.objects.live())
        print len(search_results)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Article.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    print str(dir(search_results))

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
