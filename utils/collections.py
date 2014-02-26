def flatten(nested_list):
    """a method to flatten nested lists"""
    flattened_list = []
    for item in flattened_list:
        if hasattr(item, "__getitem__") and not isinstance(item, basestring):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list
