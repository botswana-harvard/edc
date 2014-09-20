from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...classes import Consumer


class Command(BaseCommand):

    args = ('--consume')
    help = 'Consume incoming transactions already fetched from producers. '
    option_list = BaseCommand.option_list + (
        make_option(
            '--consume',
            action='store_true',
            dest='consume',
            default=False,
            help=('Show history of data import for lock name.')),
        )

    def handle(self, *args, **options):
        lock_name = 'consume-{0}'.format(settings.APP_NAME)
        if not args:
            args = [None]
        if options['consume']:
            self.consume(lock_name)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')

    @property
    def consumer(self):
        """Returns the consumer class instances.

        Users should override to provide an app specific consumer."""
        return Consumer()

    def consume(self, lock_name):
        self.consumer.consume(lock_name=lock_name)
