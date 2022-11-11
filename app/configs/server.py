from .default import DefaultConfig

class Config(DefaultConfig):
    @staticmethod
    def address(configs):
        ip = configs.get('ip')
        port = configs.get('port')
        
        return ip, int(port)
        
    @staticmethod
    def limitations(configs):
        limit = configs.get('limit')
        blocking = configs.get('blocking')
        
        return int(limit), bool(blocking)
