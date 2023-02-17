import peewee as pee

class UserExtension(metaclass=pee.Model):
    def authenticate(self, password: str):
        if self.password != password:
            raise
