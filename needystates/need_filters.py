from needystates.operations import Operations


class NeedFilter(object):
    pass


class AddressPathExactFilter(NeedFilter):

    def __init__(self, filter_object: list):
        self.filter_object = filter_object

    def check_filter(self, need):
        if need.address_path == self.filter_object:
            return True
        else:
            return False


class AddressPathContainsFilter(NeedFilter):

    def __init__(self, filter_object: str):
        self.filter_object = filter_object

    def check_filter(self, need):
        if self.filter_object in need.address_path:
            return True
        else:
            return False


class AttributeFilter(NeedFilter):

    def __init__(self, filter_object: str):
        self.filter_object = filter_object

    def check_filter(self, need):
        if need.attribute == self.filter_object:
            return True
        else:
            return False


class OperationFilter(NeedFilter):

    def __init__(self, filter_object: Operations):
        self.filter_object = filter_object

    def check_filter(self, need):
        if need.operation == self.filter_object:
            return True
        else:
            return False


class ParentStatesExactFilter(NeedFilter):
    def __init__(self, filter_object: Operations):
        self.filter_object = filter_object

    def check_filter(self, need):
        if need.parent_states == self.filter_object:
            return True
        else:
            return False


class ParentStatesContainsFilter(NeedFilter):

    def __init__(self, filter_object: str):
        self.filter_object = filter_object

    def check_filter(self, need):
        if self.filter_object in need.parent_states:
            return True
        else:
            return False


class ValueTypeFilter(NeedFilter):

    def __init__(self, filter_object):
        self.filter_object = filter_object

    def check_filter(self, need):
        if isinstance(need.value, self.filter_object):
            return True
        else:
            return False


class ValueIsFilter(NeedFilter):

    def __init__(self, filter_object):
        self.filter_object = filter_object

    def check_filter(self, need):
        if need.value == self.filter_object:
            return True
        else:
            return False