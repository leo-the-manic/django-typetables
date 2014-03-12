"""Tests for the to_object() decorator."""
import typetable


def test_stores_func_on_class():
    """The decorated method gets stored with a special alias."""

    @typetable.typetable
    class Foo:

        @typetable.to_object
        def bar(cls, a):
            pass

    assert Foo._typetable_value_to_object == Foo.bar
