from jasper.exceptions import ThenException
from jasper.utility import blue, red, grey
from functools import wraps
from collections import namedtuple


class Then(object):

    def __init__(self, function):
        self.then_function = function
        self.ran = False
        self.passed = False

    def __call__(self, context):
        context.lock()
        try:
            self.then_function(context)
        except Exception as e:
            raise ThenException(e)
        else:
            self.passed = True
        finally:
            self.ran = True

    def __str__(self):
        if not self.ran:
            color = grey
        elif self.passed:
            color = blue
        else:
            color = red

        return color(f'Then: {self.then_function.__name__}')


def then(func):
    @wraps(func)
    def wrapper(context):
        func(context)

    step = namedtuple('Step', ['cls', 'function'])
    return step(Then, wrapper)
