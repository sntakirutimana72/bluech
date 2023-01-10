from .utils.router import router

url_patterns = [
    router('POST:/session', '[<CONTROLLER>]'),
    router('DELETE:/session', '[<CONTROLLER>]'),
    router('GET:/messages', '[<CONTROLLER>]'),
    router('POST:/message', '[<CONTROLLER>]'),
    router('PATCH:/message', '[<CONTROLLER>]'),
    router('DELETE:/message', '[<CONTROLLER>]'),
    router('PATCH:/users/<id int>', '[<CONTROLLER>]'),                      # (edit display name)
    router('PUT:/users/<id int>', '[<CONTROLLER>]'),                        # (change profile picture)
    router('GET:/users', '[<CONTROLLER>]'),                                 # (fetch all users)
    router('POST:/groups', '[<CONTROLLER>]'),                               # (create group)
    router('PUT:/groups/<id int>', '[<CONTROLLER>]'),                       # (add member)
    router('DELETE:/groups/<id int>/members/<id int>', '[<CONTROLLER>]'),   # (remove member)
    router('DROP:/groups/<id int>', '[<CONTROLLER>]'),                      # (leave group)
    router('DELETE:/groups/<id int>', '[<CONTROLLER>]'),                    # (delete group)
    router('ASSIGN:/groups/<id int>/members/<id int>', '[<CONTROLLER>]'),   # (assign privilege)
    router('*', '[<NOT_FOUND>]'),
]
