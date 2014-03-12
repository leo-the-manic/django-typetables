"""A commandline interface to build fixtures for DRE project 'typetables.'"""
import argparse
import imp
import inspect
import json
import os
import sys

from django.conf import settings

from .typetable_fixture_generator import istypetable, extract_values_from_class


def extract_fixture_data(typetable_class):
    """Get a list of dicts for each value in the typetable.

    This list should be able to be converted directly to JSON or YAML for the
    fixture. The PK is set to ``None``

    """
    # must import at this level because Django isn't setup at toplevel
    from django.db.models import CharField

    # django fixtures expect "appname.modelname" for the model field.
    # __module__ will give appname as well as an extra '.models' bit
    modelname = ".".join(getattr(typetable_class, a)
                         for a in ('__module__', '__name__'))

    # remove '.models' from 'appname.models.ModelName' to get Django syntax
    modelname = modelname.replace(".models", "")

    # detect the typetable's charfield
    value_field = None
    for field in typetable_class._meta.fields:
        if isinstance(field, CharField):
            value_field = field.name
            break

    if value_field is None:
        raise ValueError("Couldn't find a CharField on the model " + modelname)

    # get typetable values
    values = extract_values_from_class(typetable_class)

    # generate a dict for each value
    return [{'model': modelname, 'pk': None, 'fields': {value_field: value}}
            for value in values]


def generate_typetable_fixtures(modules):
    """Scan each module in modules and create a typetable fixture file."""

    # collect all typetable classes
    typetables = []
    for module in modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and istypetable(obj):
                typetables.append(obj)

    # get all model data for all apps and collect into one big list
    models = sum((extract_fixture_data(tt) for tt in typetables), [])

    # dump the list as JSON to the console
    print(json.dumps(models, indent=4))


def main():
    parser = argparse.ArgumentParser(description=
                                     "Generate typetable fixtures.")
    parser.add_argument('main_app', help='Path to the Django main app (where '
                                         'settings.py is)')

    args = parser.parse_args()

    project_root = os.path.join(args.main_app, os.pardir)
    project_root = os.path.normpath(project_root)
    sys.path.append(project_root)

    # setup the django 'environ' to allow importing models
    settings_module = imp.find_module('settings', [args.main_app])
    settings_mod = imp.load_module('settings', *settings_module)
    settings.configure(settings_mod)

    # scan for all models.py files
    modules = []
    for name in os.listdir(project_root):

        # only do installed apps
        if not name in settings_mod.INSTALLED_APPS:
            continue

        # skip the main app
        if name == args.main_app:
            continue

        appname = name
        app_path = os.path.join(project_root, appname)
        app_path = os.path.normpath(app_path)

        app_module = imp.find_module(appname, [project_root])

        # see if the module exists
        try:
            models_module = imp.find_module('models', [app_path])
        except ImportError:
            pass
        else:
            # import the containing app first, to allow package-relative
            # imports in the models file
            imp.load_module(appname, *app_module)

            # import the 'models' module
            mod = imp.load_module('.'.join((appname, 'models')),
                                  *models_module)
            modules.append(mod)

    generate_typetable_fixtures(modules)


if __name__ == '__main__':
    main()
