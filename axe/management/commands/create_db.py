from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting db creation'))
        dbname = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        try:
            con = None
            con = connect(dbname='postgres', user=user, host=host, password=password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('CREATE DATABASE ' + dbname)
        except Exception as cerror:
            self.stdout.write(self.style.ERROR(f'{cerror}'))
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

        self.stdout.write(self.style.SUCCESS('All Done'))