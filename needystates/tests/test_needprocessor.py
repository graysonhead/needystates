from unittest import TestCase
from needystates.handler import need_handler
from needystates.need_filters import *
from needystates import NeedProcessor, Need, StateOperations
from needystates.exceptions import NeedyStatesHandlerException


class TestNeedProcessor(TestCase):

    def test_need_handler_execution(self):
        nd = Need('test', StateOperations.SET, address_path=['addr'], value='testval')
        np = NeedProcessor()
        @need_handler(AddressPathExactFilter(['addr']), AddressPathContainsFilter('addr'))
        def handle_need(need):
            pass
        np.add_handler(handle_need)
        np.add_need(nd)
        np.handle_needs()
        self.assertEqual([], np.unsated_needs)
        self.assertEqual([nd], np.sated_needs)

    def test_add_need(self):
        nd = Need('test', StateOperations.SET, address_path=['addr'], value='testval')
        np = NeedProcessor()
        np.add_need(nd)
        self.assertEqual([nd], np.unsated_needs)

    def test_add_multiple_needs(self):
        nd1 = Need('test1', StateOperations.SET, address_path=['addr'], value='testval')
        nd2 = Need('test2', StateOperations.SET, address_path=['addr'], value='testval')
        np = NeedProcessor()
        np.add_needs([nd1, nd2])
        self.assertEqual([nd1, nd2], np.unsated_needs)

    def test_exception_handling(self):
        nd = Need('test', StateOperations.SET, address_path=['addr'], value='testval')
        np = NeedProcessor()

        @need_handler(AddressPathExactFilter(['addr']), AddressPathContainsFilter('addr'))
        def raise_error(need):
            raise Exception("Test Exception")

        np.add_handler(raise_error)
        np.add_need(nd)
        with self.assertRaises(NeedyStatesHandlerException):
            np.handle_needs()

