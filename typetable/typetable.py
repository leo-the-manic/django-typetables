from django.db.models import CharField, Manager

from . import dreapp_meta


def _model_is_typetable(model):
    """Check if ``model`` is a typetable."""
    try:
        return model.__metaclass__.__func__ == typetable
    except BaseException:
        return False


def make_manager(typetable_field):
    """Get a custom Manager subclass for a typetable with the given field.

    :param typetable_field: the name of the typetable's descriptive field.

    :return:
        A Django ``Manager`` subclass. For more information, `see here`__.

    __ https://docs.djangoproject.com/en/dev/topics/serialization/
       #deserialization-of-natural-keys

    """

    class TypetableManager(Manager):

        def get_by_natural_key(self, string):
            kwargs = {typetable_field: string}
            return self.get(**kwargs)

    return TypetableManager


def make_naturalkey_method(typetable_field):
    """Make a method suitable as ``natural_key()`` for a Typetable.

    :param typetable_field:
        The name of the typetable's readable string field.

    The ``natural_key`` method is described `here`__.

    __ https://docs.djangoproject.com/en/dev/topics/serialization/
       #serialization-of-natural-keys

    """

    def natural_key(inst):
        return (getattr(inst, typetable_field),)
    return natural_key


def typetable(class_name, parents, attrs):
    """A metaclass to create type tables.

    This will:

    - add a ``CharField`` to the class. The field name is the class name, but
      converted from ``PascalCase`` to ``lowercase_underscore``.

    - add an inner ``Meta`` class which sets ``db_table`` to a
      pluralized version of the field name.

    - add an auto-incrementing integer primary key field named by
      appending ``_id`` to the end of the field name.

    - provide a ``__str__`` method which will simply return the ``CharField``.

    - provides a custom ``Manager`` subclass to allow serialization to work
      based on a typetable value. This is so that typetables which have already
      had data records loaded can be kept in sync with new changes using the
      ``syncdata`` command from django-extensions_. For more information on
      custom managers, `see here`__.

    __ https://docs.djangoproject.com/en/dev/topics/serialization/
       #deserialization-of-natural-keys

    For the table name, pluralization is simplistic: it simply adds the letter
    's' to the end of the string. If that's not sufficient, add a ``_plural``
    attribute to your class and that will be used instead.  ``_plural`` will be
    used verbatim so it should be in ``lowercase_underscore`` format. Also, if
    no ``_plural`` is defined but a ``Meta`` with ``verbose_name_plural`` is
    defined, that verbose name will be convereted to ``lowercase_underscore``
    format and used.

    For more information, see :doc:`/typetables`.

    .. note::
        This function shouldn't be called directly. Instead it should be used
        as the ``__metaclass__`` value for a class or module. The official
        Python documentation has information on metaclasses, and `this
        StackOverflow answer`_ is also a good resource.

    For example: ::

        from django.db.models import Model
        from dre_webapp.util import typetable

        class Gender(Model):
            __metaclass__ = typetable

    will result in a class that's equivalent to the following: ::

        from django.db.models import Manager, Model, CharField, AutoField

        class Gender(Model):

            objects = make_manager('gender')

            id = AutoField(primary_key=True, db_column='gender_id')

            gender = CharField(max_length=255)

            class Meta:
                db_table = 'genders'

            def __str__(self):
                return self.gender


    .. _this StackOverflow answer: http://stackoverflow.com/a/6581949/125415
    .. _django-extensions: https://github.com/django-extensions
                           /django-extensions

    """

    # add the char field
    field_name = dreapp_meta.clsname_to_varname(class_name)
    attrs[field_name] = CharField(max_length=255, unique=True,
                                  db_column=field_name)

    # add __str__
    attrs['__str__'] = lambda self: getattr(self, field_name)

    # add an 'ordering' field
    dreapp_meta.add_innermeta(class_name, attrs)
    attrs['Meta'].ordering = [field_name]

    # add the object manager
    mgr = make_manager(field_name)
    attrs.update(objects=mgr())

    # add the natural_key method
    attrs['natural_key'] = make_naturalkey_method(field_name)

    # create the new class
    # inner import to prevent cyclic importing
    from .dreapp_meta import DreAppMetaclass
    cls = DreAppMetaclass(class_name, parents, attrs)
    return cls
