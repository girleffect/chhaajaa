from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter

# "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('p', PagesAPIViewSet)