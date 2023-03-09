def get_attribute_values(abs_obj, only=None, exceptions=None):
    if only is None:
        only = abs_obj.__all__
    if exceptions:
        only = filter_with_exc(only, exceptions)
    yield from map(abs_obj.__dict__.get, only)

def filter_dict_items(dict_obj, only=None):
    if only is None:
        only = []
    return dict(filter(lambda els: els[0] in only, dict_obj.items()))

def filter_with_exc(original_iter, exceptions=None):
    if exceptions is None:
        exceptions = []
    return filter(lambda k: k not in exceptions, original_iter)
