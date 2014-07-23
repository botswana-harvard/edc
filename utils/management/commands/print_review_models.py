from django.core.management.base import BaseCommand, CommandError

from utils import generate_review_models


class Command(BaseCommand):
    args = 'full_app_name'
    help = 'Print review model code for a given app.'

    def handle(self, *args, **kwargs):
        if not args:
            raise CommandError("missing argument <app_name>, e.g. app.bcpp_subject.")
        generate_review_models(args[0])
