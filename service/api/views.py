from wagtail.api.v2.views import BaseAPIViewSet

from .filters import CustomFieldsFilter, CategoryFilter, LocationFilter, ConcernFilter
from ..models import ServicePage


class ServicesAPIViewSet(BaseAPIViewSet):
    """API viewset for custom API endpoint 'services'"""

    name = "services"
    model = ServicePage

    body_fields = BaseAPIViewSet.body_fields + [
        "name",
    ]

    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        "name",
    ]
    nested_default_fields = BaseAPIViewSet.nested_default_fields + [
        "name",
    ]

    meta_fields = ["type"]

    filter_backends = [
        CustomFieldsFilter,
        CategoryFilter,
        LocationFilter,
        ConcernFilter,
    ]

    known_query_parameters = BaseAPIViewSet.known_query_parameters.union(
        [
            "category",
            "location",
            "concern",
        ]
    )
