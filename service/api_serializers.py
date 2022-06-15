from rest_framework.fields import Field


class CategorySerlializer(Field):
  def to_representation(self, value):
    return value.name


# class ConcernSerlializer(Field):
#   def to_representation(self, value):
#     intros = []
#     print(value)
#     return intros