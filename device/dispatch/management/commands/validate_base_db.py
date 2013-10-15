import logging
from django.core.management.base import BaseCommand, CommandError
from apps.bcpp_dispatch.classes import PrepareDevice


logger = logging.getLogger(__name__)

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<source> <destination>'
    help = 'Validates netbook bases database has all required edc common data for dispatch.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')
        source = args[0]
        destination = args[1]
        step = 0
        if len(args) == 3:
            step = args[2]
        validate_base = PrepareDevice(source,
                                      destination,
                                      exception=CommandError,
                                      preparing_netbook=True)
        validate_base.validate_base(step=step)
