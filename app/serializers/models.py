__all__ = (
    'ModelSerializer',
    'ListQuerySerializer',
    'UserSerializer',
    'MessageSerializer',
    'UserListQuerySerializer',
    'MessageListQuerySerializer'
)

import peewee as pee
import typing as yi

class ModelSerializer(object):
    fields: tuple[tuple[str, str]]
    includes: dict[str, yi.Any] | None = None

    def __init__(self, resource: pee.Model, **kwargs):
        self.resource = resource
        self.kwargs = kwargs

    @property
    def to_json(self):
        container = {}
        for (name, prefer) in self.fields:
            if hasattr(self, prefer):
                original = getattr(self, prefer)
            else:
                original = getattr(self.resource, name)
            if self.includes and name in self.includes:
                serializer: yi.Type[ModelSerializer | ListQuerySerializer] = self.includes[name]
                container[prefer] = serializer(original).to_json
            else:
                container[prefer] = original
        return container

class ListQuerySerializer(object):
    Serializer: yi.Type[ModelSerializer]

    def __init__(self, query: pee.Query, **kwargs):
        self.query = query
        self.kwargs = kwargs

    @property
    def to_json(self):
        return [self.Serializer(res, **self.kwargs).to_json for res in self.query]

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

class AllMessageSerializer(MessageSerializer):
    includes = None

    @property
    def sender(self):
        sender = self.resource.sender.id
        return sender if sender != self.kwargs['current_user'] else None

class UserListQuerySerializer(ListQuerySerializer):
    Serializer = UserSerializer

class MessageListQuerySerializer(ListQuerySerializer):
    Serializer = AllMessageSerializer
