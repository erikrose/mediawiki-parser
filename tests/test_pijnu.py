"""Tests that should be part of pijnu and will be as soon as we get around to setting up a test framework for it"""

from mediawiki_parser.tests import ParserTestCase
from mediawiki_parser.wikitextParser import make_parser


class CustomToolsetTests(ParserTestCase):
    """Tests for custom formatting functions"""

    def test_italic(self):
        """Make sure plugging in a custom quote-parsing postprocessor works."""
        def parse_all_quotes(node):
            node.value = 'kaboom'
        parser = make_parser({'parse_all_quotes': parse_all_quotes})
        source = "Here, we have ''italic'' text."
        result = "[rawText:'kaboom']"
        self.assertEquals(unicode(parser.inline.parseTest(source).value), result)
