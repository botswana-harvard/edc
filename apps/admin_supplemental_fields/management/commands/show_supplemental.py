from django.core.management.base import BaseCommand, CommandError

from ...utils import show_supplemental_fields


class Command(BaseCommand):

    args = ''
    help = 'Show admin classes using Supplemental Fields'

    def handle(self, *args, **options):
        show_supplemental_fields()
