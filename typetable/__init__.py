registered_typetables = []


__TYPETABLE_CONVERTER_MARKER = '_typetable_value_converter'


def typetable(cls):
    registered_typetables.append(cls)

    # search for a value converter and mark it
    for name, val in cls.__dict__.items():
        if hasattr(val, __TYPETABLE_CONVERTER_MARKER):
            cls._typetable_value_to_object = val
            break

    return cls


class Value:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __get__(self, obj, type=None):
        raise type.DoesNotExist()


def to_object(meth):
    meth = classmethod(meth)
    setattr(meth, __TYPETABLE_CONVERTER_MARKER, True)
    return meth


class SimpleTypeTable:
    pass


def install(table):
    """Create all Value instances for the given typetable."""
    values = (v for k, v in table.__dict__.items() if isinstance(v, Value))
    factory = table._typetable_value_to_object
    for value in values:
        instance = factory(*value.args, **value.kwargs)
        instance.save()
