import time

from django.db import connections
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause execution until DB is available.
    """
    def handle(self, *args, **options):

        # TODO: Handle all database connections instead of just default.
        self.stdout.write('Waiting for db.')
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stdout.write('DB is currently unavailable. Waiting 1 second.')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available.'))
