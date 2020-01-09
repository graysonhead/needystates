class NeedyStatesException(Exception):
    pass


class NeedyStatesHandlerException(NeedyStatesException):
    pass


class NeedyStatesNoMatch(NeedyStatesHandlerException):
    pass