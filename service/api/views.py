from wagtail.api.v2.views import BaseAPIViewSet

from ..models import ServicePage
from ..snippets import ServiceCategory
from .filters import CustomFieldsFilter, CategoryFilter, LocationFilter


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
    ]

    known_query_parameters = BaseAPIViewSet.known_query_parameters.union(
        [
            "category",
            "location",
            "concern",
        ]
    )