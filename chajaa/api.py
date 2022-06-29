from wagtail.api.v2.router import WagtailAPIRouter

from service.api.views import ServicesAPIViewSet


# "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

# custom endpoint for services
api_router.register_endpoint("services", ServicesAPIViewSet)
