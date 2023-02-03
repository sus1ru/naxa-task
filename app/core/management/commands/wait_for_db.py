"""
Django custom command to deal with the racing condition while postgres
initialization(wait for the DB to available).
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for the DB to available """
    def handle(self, *args, **options):
        """ Entry point for the django command """
        self.stdout.write('Getting the database ready...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('DB not ready yet, waiting a second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database Ready!!'))
