import typetable


def test_decorator_adds_class_to_registry():
    """Typetables are added to a central registry."""

    class Foo:
        pass

    assert Foo not in typetable.registered_typetables
    typetable.typetable(Foo)
    assert Foo in typetable.registered_typetables
