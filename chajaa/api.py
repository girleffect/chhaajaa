from wagtail.api.v2.views import BaseAPIViewSet, FieldsFilter
from wagtail.api.v2.router import WagtailAPIRouter

from service.models import ServicePage


class ServicesViewSet(BaseAPIViewSet):
    model = ServicePage
    filter_backends = [
      FieldsFilter
    ]

# "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

api_router.register_endpoint("services", ServicesViewSet)