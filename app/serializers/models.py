__all__ = (
    'ModelSerializer',
    'ModelListQuerySerializer',
    'UserSerializer',
)

import peewee as pee
import typing as yi

class ModelSerializer(object):
    fields: tuple[tuple[str, str]]
    joins: list[yi.Type[pee.Model]] = []
    includes: dict[str, yi.Any] = {}

    def __init__(self, resource: pee.Model):
        self.resource = resource

    @property
    def to_json(self):
        container = {}
        # fix N+1 querying issue
        if self.joins:
            self.resource.joins(self.joins)
        for (name, prefer) in self.fields:
            # override if there is a property of the same name
            if hasattr(self, prefer):
                original = getattr(self, prefer)
            else:
                original = getattr(self.resource, name)
            # apply another serializer to the field/attribute
            if name in self.includes:
                serializer: yi.Type[ModelSerializer | ModelListQuerySerializer] = self.includes[name]
                container[prefer] = serializer(original).to_json
            else:
                container[prefer] = original
        return container


class ModelListQuerySerializer(object):
    serializer: yi.Type[ModelSerializer]

    def __init__(self, query: pee.Query):
        self.query = query

    @property
    def to_json(self):
        return [self.serializer(resource) for resource in self.query]

class UserSerializer(ModelSerializer):
    fields = (
        ('id', 'id'),
        ('email', 'email'),
        ('nickname', 'nickname'),
    )
