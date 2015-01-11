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


class String(Typed):
    ty = str

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
        super(String, self).__init__()

    def __set__(self, instance, value):
        ''' This will ensure that the min and max values are proper and that the
        type is a string
        '''
        if self.min and len(value) < self.min:
            raise TypeError('Must be >= %d' % self.min)
        if self.max and len(value) > self.max:
            raise TypeError('Must be <= %d' % self.max)
        super(String, self).__set__(instance, value)


class YearOfStudy(Typed):
    ty = int

    def __init__(self, min, max):
        self.min = min
        self.max = max
        super(YearOfStudy, self).__init__()

    def __set__(self, instance, value):
        if self.min and value < self.min:
            raise TypeError('Must be >= %d' % self.min)
        if self.max and value > self.max:
            raise TypeError('Must be <= %d' % self.max)
        super(YearOfStudy, self).__set__(instance, value)


class IntString(String):
    '''
    A string that can be converted to an integer
    '''
    def __init__(self, **kwargs):
        super(IntString, self).__init__(**kwargs)

    def __set__(self, instance, value):
        try:
            int(value)
        except ValueError:
            raise ValueError('Must be convertable to integer' % self.max)
        super(IntString, self).__set__(instance, value)


class PasswordString(String):
    def __set__(self, instance, value):
        ''' Password rules:
        1. No special characters allowed
        2. Space not allowed
        3. Min 6 Max 20
        4. At least one numeric character
        5. At least one capital letter
        6. Only two repetitive characters allowed
        '''
        s = '^(?=.*[A-Z])(?=.*\d)(?!.*(.)\1\1)[a-zA-Z0-9@]{6,20}$'
        print(s)
        if not re.match(s, value):
            raise TypeError('Password does not meet minimum requirements')
        super(PasswordString, self).__set__(instance, value)
