from datetime import datetime


def find_errors(values, required_items=list(), dates=list()):
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
    vals = {'a': ['required', 'date', 'len_min 3', 'len_max 4']}
    errors = errors + required(values, required_items)
    errors = errors + valid_dates(values, dates)
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
        if item not in values:
            errors.append(item + " is required")
    return errors


def valid_dates(dates):
    """
        >>> valid_dates(['2014-03-02 18H00'])
        []
        >>> valid_dates(['2012-03-02 00H00'])
        []
        >>> valid_dates(['201-03-02 18H00'])
        ['invalid date: 201-03-02 18H00']
        >>> valid_dates(['2012-0-02 18H00'])
        ['invalid date: 2012-0-02 18H00']
        >>> valid_dates(['2012-43-02 18H00'])
        ['invalid date: 2012-43-02 18H00']
        >>> valid_dates(['2012-43-02'])
        ['invalid date: 2012-43-02']
    """
    errors = list()
    for dt in dates:
        try:
            datetime.strptime(dt, "%Y-%m-%d %HH%M")
        except:
            errors.append('invalid date: {}'.format(dt))
    return errors
