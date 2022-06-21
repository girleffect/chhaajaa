from wagtail.api.v2.views import BaseAPIViewSet, FieldsFilter

from ..models import ServicePage


class ServicesAPIViewSet(BaseAPIViewSet):
    name = 'services'
    model = ServicePage
    body_fields = BaseAPIViewSet.body_fields + [
        'name',
    ]

    meta_fields = [
        'detail_url'
    ]

    filter_backends = [
        # CustomFilter
        FieldsFilter
    ]