class Models:
    
    @staticmethod
    def user(**others):
        return {'email': 'admin@email.it', 'password': '1234', 'nickname': 'admin760', **others}
    
    @staticmethod
    def channel(**others):
        return {'nickname': 'channel_728', **others}
    
    @staticmethod
    def resource(**others):
        return {'location': 'app/ext_static/images/profile.png', **others}
        
    @staticmethod
    def activity(**others):
        return {'name': 'login', **others}
        
    @staticmethod
    def activity_log(**others):
        return {'summary': ':admin logged in', **others}
