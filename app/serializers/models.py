__all__ = (
    'ModelSerializer',
    'ModelListQuerySerializer',
    'UserSerializer',
    'MessageSerializer',
)

import peewee as pee
import typing as yi

class ModelSerializer(object):
    fields: tuple[tuple[str, str]]
    includes: dict[str, yi.Any] | None = None

    def __init__(self, resource: pee.Model):
        self.resource = resource

    @property
    def to_json(self):
        container = {}
        for (name, prefer) in self.fields:
            # override if there is a property of the same name
            if hasattr(self, prefer):
                original = getattr(self, prefer)
            else:
                original = getattr(self.resource, name)
            # apply another serializer to the field/attribute
            if self.includes and name in self.includes:
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

class MessageSerializer(ModelSerializer):
    fields = (
        ('id', 'id'),
        ('description', 'description'),
        ('is_edited', 'is_edited'),
        ('sender', 'sender'),
        ('created_at', 'sent_date'),
        ('updated_at', 'last_update')
    )
    includes = {'sender': UserSerializer}

    @property
    def sent_date(self):
        return self.resource.created_at.strftime('%Y-%b-%d %H:%M')

    @property
    def last_update(self):
        return self.resource.updated_at.strftime('%Y-%b-%d %H:%M')
