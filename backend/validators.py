def find_errors(values, required_items=list()):
    """
        simple tests:
        >>> find_errors(['a'])
        []
        >>> find_errors(['a'], ['a'])
        []
        >>> find_errors(['a'], ['b'])
        ['b is required']
    """
    errors = list()
    errors = errors + required(values, required_items)
    return errors


def length(field, min=-1, max=-1, message=None):
    errors = list()
    if field is None:
        return
    length = len(field)
    if not message:
        message = u'Field must be between %i and %i characters' % (min, max)
    if length < min or max != -1 and length > max:
        errors.append(field + " is too short/long")


def required(values, required_items=list()):
    errors = list()
    for item in required_items:
        if item not in values or not values[item]:
            errors.append(item + " is required")
    return errors
