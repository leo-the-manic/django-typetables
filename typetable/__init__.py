def typetable(cls):
    return cls


class Value:

    def __init__(self, *args):
        pass

    def __get__(self, obj, type=None):
        raise type.DoesNotExist()


def to_object(*args):
    pass


class SimpleTypeTable:
    pass
