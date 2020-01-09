from functools import wraps
from .exceptions import NeedyStatesNoMatch


def need_handler(*filter_args):
    def wrapper(func):
        @wraps(func)
        def inner(need):
            if all([i.check_filter(need) for i in filter_args]):
                return func(need)
            else:
                raise NeedyStatesNoMatch
        return inner
    return wrapper






