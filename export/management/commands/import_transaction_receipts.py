import json

from datetime import datetime

from django.core import serializers
from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError

from edc.core.crypto_fields.classes import FieldCryptor
from edc.export.models.export_transaction import ExportTransaction
from edc.notification.models import Notification, NotificationPlan

from ...classes import ExportJsonAsCsv
from ...models import ExportPlan
from django.contrib.webdesign.lorem_ipsum import sentence


class Command(BaseCommand):

    args = '<receipt filename>'
    help = 'Import a receipt file for recently exported transactions.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        export_json_as_csv = None
