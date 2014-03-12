from unittest import TestCase

from ..typetable_fixture_generator import (extract_values_from_string,
                                           find_values_string,
                                           get_docstring_lines, istypetable)


class ExampleTypetable(object):
    """Example class definition used in the unit tests below.

    A type table.

    Example values are 'foo' and 'bar.'
    """
    pass


class TypetableDetectorTest(TestCase):

    def test_detect_typetable(self):
        """Ensure typetables get detected by ``istypetable``."""
        self.assertTrue(istypetable(ExampleTypetable))

    def test_reject_nontypetable(self):
        """Ensure non-typetables are rejected by ``istypetable``."""

        class Foo(object):
            """Definitely not a type table."""
            pass

        self.assertFalse(istypetable(Foo))


class ExtractValuesTest(TestCase):

    def test_extracts_values(self):
        """Ensure ``extract_values_from_string`` gets the correct values."""

        docstr1 = "Example values are 'foo' and 'bar.'"
        values = extract_values_from_string(docstr1)
        self.assertEqual(values, ['foo', 'bar'])

        docstr2 = "Example values are 'biz,' 'buz' and 'baz.'"
        values2 = extract_values_from_string(docstr2)
        self.assertEqual(values2, ['biz', 'buz', 'baz'])

    def test_chooses_correct_line(self):
        """Ensure the value extractor function detects the proper line."""

        # create a class where the 'Example values are' line isn't the only
        # line in the docstring
        class TypetableExample(object):
            """This is line isn't really 'important,' you know?

            This next line is:

            Example values are 'foo' and 'bar'.
            """

        string = find_values_string(TypetableExample.__doc__)
        self.assertEqual(string, "Example values are 'foo' and 'bar'.")


class DocstringSplitterTest(TestCase):

    def test_splits_multiline_docstring(self):
        docstring_lines = get_docstring_lines("""Hello.

        foo

        bar""")

        self.assertEqual(docstring_lines, ["Hello.", "foo", "bar"])

    def test_no_trailing_space(self):
        """Ensure that there is no trailing whitepsace."""
        docstring_lines = get_docstring_lines("""foo

        bar
        """)

        self.assertEqual(docstring_lines, ['foo', 'bar'])


    def test_multiline_paragraph(self):
        docstr = """This paragraph is
        on multiple lines."""

        lines = get_docstring_lines(docstr)
        self.assertEqual(lines, ['This paragraph is on multiple lines.'])


class FindValuesStrTest(TestCase):

    def test_multiline_values_paragraph(self):
        """Ensure that multiline value lists are returned properly."""
        vals = find_values_string("""Example values are 'foo,'
            'bar,' and 'bazz.'""")
        self.assertEqual(vals, "Example values are 'foo,' 'bar,' and 'bazz.'")

