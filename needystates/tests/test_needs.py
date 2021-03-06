from needystates import StateOperations
from needystates import Need
from unittest import TestCase


class TestNeeds(TestCase):

    def test_need_string_generation_emptyvalues(self):
        nd = Need('url', StateOperations.SET, value='https://example.com')
        result = nd.get_short_string()
        self.assertEqual('url.SET=https://example.com', result)

    def test_need_string_generation_novalue(self):
        nd = Need('url', StateOperations.DELETE)
        result = nd.get_short_string()
        self.assertEqual('url.DELETE', result)

    def test_need_string_generation(self):
        nd = Need('url', StateOperations.SET, address_path=['dbconfmodule', 'dbConfigManager'],
                  parent_states=['server'], value='https://example.com')
        result = nd.get_short_string()
        self.assertEqual('dbconfmodule.dbConfigManager|server.url.SET=https://example.com', result)

    def test_long_string_generation(self):
        nd = Need('url', StateOperations.SET, value='https://example.com',
                  description="This sets and does things with other things braaaah")
        result = nd.get_long_string()
        self.assertEqual('url.SET=https://example.com\n----------\nThis sets and does things with other things braaaah',
                         result)