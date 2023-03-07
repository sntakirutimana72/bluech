def get_attribute_values(abs_obj, only=[], exceptions=[]):
    if not only:
        only = abs_obj.__all__
    if exceptions:
        only = filter_with_exc(only, exceptions)
    yield from map(abs_obj.__dict__.get, only)
    
def filter_dict_items(dict_obj, only=[]):
    return dict(filter(lambda els: els[0] in only, dict_obj.iteritems()))

def filter_with_exc(original_iter, exceptions=[]):
    return filter(lambda k: k not in exceptions, original_iter)
