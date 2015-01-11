from __future__ import print_function
from weakref import WeakKeyDictionary
import re


class Descriptor(object):
    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance, None)

    def __set__(self, instance, value):
        self.data[instance] = value

    def __delete__(self, instance):
        del self.data[instance]


class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError('Expected %s instead of %s' % (self.ty,
                                                           value.__class__))
        super(Typed, self).__set__(instance, value)


class Ranged(Descriptor):
    def __init__(self, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        super(Ranged, self).__init__(**kwargs)

    def __set__(self, instance, value):
        if self.min and value < self.min:
            raise TypeError('Must be >= %d' % self.min)
        if self.max and value > self.max:
            raise TypeError('Must be <= %d' % self.max)
        super(Ranged, self).__set__(instance, value)


class Sized(Descriptor):
    def __init__(self, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        super(Sized, self).__init__(**kwargs)

    def __set__(self, instance, value):
        if self.min and len(value) < self.min:
            raise TypeError('Must be >= %d' % self.min)
        if self.max and len(value) > self.max:
            raise TypeError('Must be <= %d' % self.max)
        super(Sized, self).__set__(instance, value)


class String(Typed):
    ty = str


class SizedString(String, Sized):
    pass


class IntSizedString(SizedString):
    '''
    A string that can be converted to an integer
    '''
    def __init__(self, **kwargs):
        super(IntSizedString, self).__init__(**kwargs)

    def __set__(self, instance, value):
        try:
            int(value)
        except ValueError:
            raise ValueError('Must be convertable to integer' % self.max)
        super(IntSizedString, self).__set__(instance, value)


class Regex(Descriptor):
    def __init__(self, *args, **kwargs):
        self.pattern = re.compile(kwargs.pop('pattern'))
        super(Regex, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pattern.match(value):
            raise ValueError('Invalid string')
        super(Regex, self).__set__(instance, value)


class YearOfStudy(Typed, Ranged):
    ty = int


class PasswordString(SizedString, Regex):
    pass


class RegexString(String, Regex):
    pass
