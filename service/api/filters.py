from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.filters import BaseFilterBackend
from taggit.managers import TaggableManager

from wagtail.api.v2.utils import BadRequestError, parse_boolean

from ..snippets import ServiceCategory, ServiceLocation, ConcernPage


class CustomFieldsFilter(BaseFilterBackend):
    """
    A subclass of the BaseFilterBackend. Allows querying the service by location, category, and concern names rather than IDs.
    """

    def filter_queryset(self, request, queryset, view):
        """
        This performs field level filtering on the result set
        Eg: ?title=James Joyce
        """
        fields = set(view.get_available_fields(queryset.model, db_fields_only=True))

        # Locale is a database field, but we provide a separate filter for it
        # Category, location, and concern, have their look_up field set to id
        # so we provide separate filters for them too.
        if "locale" in fields:
            fields.remove("locale")
        if "category" in fields:
            fields.remove("category")
        if "location" in fields:
            fields.remove("location")
        if "concern" in fields:
            fields.remove("concern")

        for field_name, value in request.GET.items():
            if field_name in fields:
                try:
                    field = queryset.model._meta.get_field(field_name)
                except LookupError:
                    field = None

                # Convert value into python
                try:
                    if isinstance(
                        field, (models.BooleanField, models.NullBooleanField)
                    ):
                        value = parse_boolean(value)
                    elif isinstance(field, (models.IntegerField, models.AutoField)):
                        value = int(value)
                    elif isinstance(field, models.ForeignKey):
                        value = field.target_field.get_prep_value(value)

                except ValueError as e:
                    raise BadRequestError(
                        "field filter error. '%s' is not a valid value for %s (%s)"
                        % (value, field_name, str(e))
                    )

                if isinstance(field, TaggableManager):
                    for tag in value.split(","):
                        queryset = queryset.filter(**{field_name + "__name": tag})

                    # Stick a message on the queryset to indicate that tag filtering has been performed
                    # This will let the do_search method know that it must raise an error as searching
                    # and tag filtering at the same time is not supported
                    queryset._filtered_by_tag = True
                else:
                    queryset = queryset.filter(**{field_name: value})

        return queryset


class CategoryFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """Custom filter for category"""
        if "category" in request.GET:
            _filtered_by_child_of = getattr(queryset, "_filtered_by_child_of", None)

            queryset = queryset.filter(category__name__iexact=request.GET["category"])

            if _filtered_by_child_of:
                queryset._filtered_by_child_of = _filtered_by_child_of

        return queryset


class LocationFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """Custom filter for location"""
        if "location" in request.GET:
            _filtered_by_child_of = getattr(queryset, "_filtered_by_child_of", None)

            queryset = queryset.filter(location__name__iexact=request.GET["location"])

            if _filtered_by_child_of:
                queryset._filtered_by_child_of = _filtered_by_child_of

        return queryset


class ConcernFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """Custom filter for concern"""
        if "concern" in request.GET:
            _filtered_by_child_of = getattr(queryset, "_filtered_by_child_of", None)

            queryset = queryset.filter(concern__intro__iexact=request.GET["concern"])

            if _filtered_by_child_of:
                queryset._filtered_by_child_of = _filtered_by_child_of

        return queryset
