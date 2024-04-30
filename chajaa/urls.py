from os import environ
from wagtail.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.http import JsonResponse
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls import url
from search import views as search_views
from blog import views as blogsearch
from .api import api_router
from .feeds import *


def health(request):
    app_id = environ.get('MARATHON_APP_ID', None)
    ver = environ.get('MARATHON_APP_VERSION', None)
    return JsonResponse({'id': app_id, 'version': ver})


urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('api/v1/', api_router.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path("", include("social_django.urls", namespace="social")),
    path('search/', search_views.search, name='search'),
    path('blogsearch/', blogsearch.search, name='blogsearch'),
    path('health/', health, name='health'),
    re_path(r'^robots\.txt', include('robots.urls')),
    path('sitemap.xml', sitemap),
    url(r'rss/', RssFeed(), name='rssfeed'),
    url(r'atom/', AtomFeed(), name='atomfeed'),
    path("i18n/", include("django.conf.urls.i18n")),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
