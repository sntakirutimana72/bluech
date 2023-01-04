class ArgumentParser(object):
    def __init__(**vars):
        self._vars = vars
        
    def number(key, default = None):
        value = self.fetch(key, default)
        if value:
            return int(value)
            
    def boolean(key, default = None):
        value = self.fetch(key, default)
        return bool(value)
            
    def fetch(key, default = None):
        return self._vars.get(key, default)
        
        
class ServerArgumentParser(ArgumentParser):
    def address():
        ip = self.fetch('ip')
        port = self.number('port')
        return ip, port
        
    def limitations():
        limit = self.number('limit')
        blocking = self.boolean('blocking')
        return limit, blocking
