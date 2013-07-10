class ValidationError(Exception):
    pass


def length(field, min=-1, max=-1, message=None):
    if field is None:
        return
    length = len(field)
    if not message:
        message = u'Field must be between %i and %i characters' % (min, max)
    if length < min or max != -1 and length > max:
        raise ValidationError(message + " length is " + str(length))


def required(value, required=True, message=None):
    if not message:
        message = u'Field is required'
    if not value and required:
        raise ValidationError(message)


if __name__ == "__main__":
    try:
        length(5, 1, 4)
    except ValidationError as e:
        print "Oops! " + e.message

    try:
        required(None)
    except ValidationError as e:
        print "Oops! " + e.message
