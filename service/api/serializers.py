# Custom serializers for the API for category, concern, and location fields in ServicePage

from rest_framework.fields import Field


class CategorySerlializer(Field):
    def to_representation(self, value):
        return value.name


class ConcernSerlializer(Field):
    def to_representation(self, value):
        return [c.intro for c in value.all()]


class LocationSerializer(Field):
    def to_representation(self, value):
        return [l.name for l in value.all()]
