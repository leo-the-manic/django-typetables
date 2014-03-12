import django.core.management.base

import typetable


class Command(django.core.management.base.BaseCommand):

    def handle(self, *args, **options):
        for table in typetable.registered_typetables:
            typetable.install(table)
