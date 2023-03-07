def get_attribute_values(abs_obj, *attributes: tuple[str]):
    yield from map(abs_obj, attributes)
    
def filter_dict_items(dict_object, *attributes):
    return dict((key, value) for key, value in dict_object.iteritems() if key in attributes)
