from wagtail.api.v2.views import BaseAPIViewSet

from .filters import CustomFieldsFilter, CategoryFilter, LocationFilter, ConcernFilter
from ..models import ServicePage


class ServicesAPIViewSet(BaseAPIViewSet):
    name = 'services'
    model = ServicePage

    meta_fields = [
        'detail_url'
    ]

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
