from unittest import TestCase
from needystates.need_filters import *
from needystates.need import Need
from needystates.state import StateOperations


class TestNeedFilters(TestCase):

    def test_address_path_exact_filter(self):
        need = Need('test', StateOperations.SET, address_path=['one', 'two'])
        filter = AddressPathExactFilter(['one', 'two'])
        result = filter.check_filter(need)
        self.assertEqual(True, result)

    def test_address_path_exact_filter_negative(self):
        need = Need('test', StateOperations.SET, address_path=['one', 'two'])
        filter = AddressPathExactFilter(['one'])
        result = filter.check_filter(need)
        self.assertEqual(False, result)

    def test_address_path_contains_filter(self):
        need = Need('test', StateOperations.SET, address_path=['one', 'two', 'three'])
        filter = AddressPathContainsFilter('three')
        result = filter.check_filter(need)
        self.assertEqual(True, result)

    def test_address_path_contains_negative(self):
        need = Need('test', StateOperations.SET, address_path=['one', 'two'])
        filter = AddressPathContainsFilter('three')
        result = filter.check_filter(need)
        self.assertEqual(False, result)

    def test_attribute_filter(self):
        need = Need('test', StateOperations.SET)
        filter = AttributeFilter('test')
        result = filter.check_filter(need)
        self.assertEqual(True, result)

    def test_attribute_filter_negative(self):
        need = Need('test', StateOperations.SET)
        filter = AttributeFilter('test2')
        result = filter.check_filter(need)
        self.assertEqual(False, result)

    def test_operation_filter(self):
        need = Need('test', StateOperations.SET)
        filter = OperationFilter(StateOperations.SET)
        result = filter.check_filter(need)
        self.assertEqual(True, result)

    def test_operation_filter_false(self):
        need = Need('test', StateOperations.DELETE)
        filter = OperationFilter(StateOperations.SET)
        result = filter.check_filter(need)
        self.assertEqual(False, result)