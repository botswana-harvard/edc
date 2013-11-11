import logging
import os
import sqlite3
import subprocess
from datetime import datetime
from django.db.models import Model, get_model, get_models, get_app
from django.conf import settings
from django.db.models import signals
from lis.base.model.models import BaseLabListModel, BaseLabModel, BaseLabUuidModel
from edc.core.bhp_common.utils import td_to_string
from edc.base.model.models import BaseModel
from edc.device.sync.models import BaseSyncUuidModel
from edc.base.model.models import BaseUuidModel
from edc.subject.consent.models.signals import add_models_to_catalogue
from ..exceptions import BackupError, RestoreError
from .base_prepare_device import BasePrepareDevice


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class PrepareDevice(BasePrepareDevice):

    def __init__(self, using_source,
                  using_destination,
                  **kwargs):
        """
        Args:
            using_source: settings database key for the source.
            using_destination: settings database key for the destination.
        Keywords:
            exception: exception class to use, e.g. CommandError if this is run as a management command. Default(TypeError)
        """
        super(PrepareDevice, self).__init__(using_source, using_destination, **kwargs)
        self.started = None
        self.start_time = None
        self.end_time = None

    def timer(self, done=None):
        if not self.started:
            self.started = datetime.today()
            logger.info('Starting at {0}'.format(self.started))
        self._end_timer()
        self.start_time = datetime.today()
        if done:
            logger.info("processed in {0}".format(td_to_string(datetime.today() - self.started)))

    def _end_timer(self):
        if self.start_time:
            logger.info("    ....processed in {0}".format(td_to_string(datetime.today() - self.start_time)))

    def pre_prepare(self):
        return None

    def post_prepare(self):
        return None

    def prepare(self, **kwargs):
        """Runs for all common data needed for an EDC installation.

        Keywords:
            step: if specified skip to the numbered step. default(0)
        """
        # check for outgoing transactions first
        if self.has_outgoing_transactions():
            raise self.exception("Destination has outgoing transactions. Please sync and try again.")
        step = int(kwargs.get('step', 0))
        logger.info('Starting at step {0}'.format(step))
        if not step > 1:
            self.timer()
            logger.info("1. Running pre procedures")
            self.pre_prepare()
#         if not step > 2:
#             self.timer()
#             logger.info("2. Updating content_type")
#             self.update_content_type()
#         if not step > 3:
#             self.timer()
#             logger.info("3. Updating auth...")
#             self.update_auth()
#         if not step > 5:
#             self.timer()
#             logger.info("5. Updating lists...")
#             self.update_list_models()
#         if not step > 6:
#             self.timer()
#             logger.info("6. Updating bhp variables...")
#             self.update_app_models('bhp_variables', [BaseUuidModel])
#         if not step > 7:
#             self.timer()
#             logger.info("7. Updating contenttypemap...")
#             logger.info('    ...update')
#             self.update_app_models('bhp_content_type_map', [BaseModel])
#             logger.info('    ...resize')
#             self.resize_content_type()
#             self.update_app_models('bhp_content_type_map', [BaseModel])
#             logger.info('    ...pop and sync')
#             self.sync_content_type_map()
#         if not step > 8:
#             self.timer()
#             logger.info("8. Updating appointment configuration...")
#             self.update_model(("appointment", "Configuration"), [BaseSyncUuidModel])
#         if not step > 9:
#             self.timer()
#             logger.info("9. Updating the Crypt table...")
#             self.update_model(('crypto_fields', 'crypt'),[BaseModel])
#             #logger.info('   Warning, skipping. use mysqldump for the Crypt table, bhp_crypto_crypt')
#         if not step > 10:
#             self.timer()
#             logger.info("10. Updating the visit definitions...")
#             self.update_app_models('visit_schedule', [BaseUuidModel])
#         if not step > 11:
#             self.timer()
#             logger.info("11. Updating subject identifiers...")
#             self.update_app_models('identifier', [BaseModel])
#         if not step > 12:
#             self.timer()
#             logger.info("12. Updating registered subjects...")
#             self.update_model(('registration', 'registeredsubject'), [BaseModel])
#             logger.info('   Warning, skipping. use mysqldump for the RegisteredSubject table, registration_registeredsubject')
#         if not step > 13:
#             self.timer()
#             logger.info("13. Updating consent Consent Catalogues...")
#             signals.post_save.disconnect(add_models_to_catalogue, weak=False, dispatch_uid="add_models_to_catalogue")
#             self.update_model(('consent', 'ConsentCatalogue'), [BaseSyncUuidModel])
#         if not step > 14:
#             self.timer()
#             logger.info("14. Updating consent Attached Models...")
#             self.update_model(('consent', 'AttachedModel'), [BaseSyncUuidModel],fk_to_skip=['content_type_map_id', 'consent_catalogue_id'])
#             signals.post_save.connect(add_models_to_catalogue, weak=False, dispatch_uid="add_models_to_catalogue")
#         if not step > 15:
#             self.timer()
#             logger.info("15. Updating lab test code groups from lab_test_code...")
#             self.update_model(('lab_test_code', 'TestCodeGroup'), [BaseLabListModel, BaseLabModel])
#         if not step > 16:
#             self.timer()
#             logger.info("16. Updating lab test codes from lab_test_code...")
#             self.update_model(('lab_test_code', 'TestCode'), [BaseLabListModel, BaseLabModel])
#         if not step > 17:
#             self.timer()
#             logger.info("17. Updating lab aliquot types from lab_aliquot_list...")
#             self.update_model(('lab_aliquot_list', 'AliquotType'), [BaseModel])
#         if not step > 18:
#             self.timer()
#             logger.info("18. Updating lab panel models from lab_panel...")
#             self.update_app_models('lab_panel', [BaseModel])
#         if not step > 19:
#             self.timer()
#             logger.info("19. Updating aliquot types from lab_clinic_api...")
#             self.update_model(('lab_clinic_api', 'AliquotType'), [BaseLabListModel, BaseLabModel])
#         if not step > 20:
#             self.timer()
#             logger.info("20. Updating test code groups from lab_clinic_api...")
#             self.update_model(('lab_clinic_api', 'TestCodeGroup'), [BaseLabListModel, BaseLabModel])
#         if not step > 21:
#             self.timer()
#             logger.info("21. Updating test codes from lab_clinic_api...")
#             self.update_model(('lab_clinic_api', 'TestCode'), [BaseLabListModel, BaseLabModel])
#         if not step > 22:
#             self.timer()
#             logger.info("22. Updating panel from lab_clinic_api...")
#             self.update_model(('lab_clinic_api', 'Panel'), [BaseLabListModel, BaseLabModel])
#         if not step > 23:
#             self.timer()
#             logger.info("23. Updating review from lab_clinic_api...")
#             self.update_model(('lab_clinic_api', 'Review'), [BaseLabUuidModel])
#         if not step > 24:
#             self.timer()
#             logger.info("24. Updating un-scheduled lab entry buckets from bhp_lab_entry...")
#             self.update_model(('lab_entry', 'UnscheduledLabEntryBucket'))
#         if not step > 25:
#             self.timer()
#             logger.info("25. Updating lab entry from bhp_lab_entry...")
#             self.update_model(('lab_entry', 'LabEntry'), [BaseUuidModel])
#         if not step > 26:
#             self.timer()
#             logger.info("26. Updating bhp_entry.models.entry...")
#             self.update_model(('entry', 'entry'), [BaseUuidModel])
        if not step > 27:
            self.timer()
            logger.info("27. Updating api keys...")
            self.update_api_keys()
        if not step > 28:
            self.timer()
            logger.info("28. Running post procedures...")
            self.post_prepare()
        logger.info("Done")
        self.timer(done=True)

    def validate_base(self, **kwargs):
        # logger.setLevel(logging.INFO)
        """Checks to ensure that all required common EDC data for creating a base database is present"""
        if self.has_outgoing_transactions():
            # raise TypeError("Destination has outgoing transactions. Please sync and try again.")
            pass
        step = int(kwargs.get('step', 0))
        # logger.info('Starting at step {0}'.format(step))
        print 'Starting at step {0}'.format(step)
        count = 0
#       if not step > 1:
#          self.timer()
#            logger.info("1. Running pre procedures")
#            self.pre_prepare()
        print 'SOURCE : ' + self.get_using_source()
        print 'DESTINATION : ' + self.get_using_destination()
        if not step > 1:
            ContentType = get_model('contenttypes', 'ContentType')
            in_destination = ContentType.objects.using(self.get_using_destination()).all().count()
            in_source = ContentType.objects.using(self.get_using_source()).all().count()
            print "1. checking content_type. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("1. checking content_type. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 2:
            for model in get_models(get_app('auth')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "2.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("2. checking {1}. {2} objects in destination, {3} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 3:
            ApiKeys = get_model('tastypie', 'apikey')
            in_destination = ApiKeys.objects.using(self.get_using_destination()).all().count()
            in_source = ApiKeys.objects.using(self.get_using_source()).all().count()
            print "3. checking ApiKeys. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("3. checking ApiKeys. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 4:
            for model in self.return_all_list_models():
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "4.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("4. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 5:
            for model in get_models(get_app('bhp_variables')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "5.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("5. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 6:
            for model in get_models(get_app('bhp_content_type_map')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "6.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("6. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 7:
            configutations = get_model('appointment', 'Configuration')
            in_destination = configutations.objects.using(self.get_using_destination()).all().count()
            in_source = configutations.objects.using(self.get_using_source()).all().count()
            print "7. checking appointment configutations. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("7. checking appointment configutations. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 8:
            crypt = get_model('crypto_fields', 'crypt')
            in_destination = crypt.objects.using(self.get_using_destination()).all().count()
            in_source = crypt.objects.using(self.get_using_source()).all().count()
            print "8. checking crypt. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("8. checking crypt. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 9:
            for model in get_models(get_app('visit_schedule')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "9.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("9. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 10:
            for model in get_models(get_app('identifier')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "10.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("10. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 0
            count = 0
        if not step > 11:
            registeredsubject = get_model('registration', 'registeredsubject')
            in_destination = registeredsubject.objects.using(self.get_using_destination()).all().count()
            in_source = registeredsubject.objects.using(self.get_using_source()).all().count()
            print "11. checking registeredsubject. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("11. checking registeredsubject. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 12:
            consent = get_model('consent', 'ConsentCatalogue')
            in_destination = consent.objects.using(self.get_using_destination()).all().count()
            in_source = consent.objects.using(self.get_using_source()).all().count()
            print "12. checking ConsentCatalogue. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("12. checking ConsentCatalogue. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 13:
            AttachedModel = get_model('consent', 'AttachedModel')
            in_destination = AttachedModel.objects.using(self.get_using_destination()).all().count()
            in_source = AttachedModel.objects.using(self.get_using_source()).all().count()
            print "13. checking AttachedModel. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("13. checking AttachedModel. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 14:
            TestCodeGroup = get_model('lab_test_code', 'TestCodeGroup')
            in_destination = TestCodeGroup.objects.using(self.get_using_destination()).all().count()
            in_source = TestCodeGroup.objects.using(self.get_using_source()).all().count()
            print "14. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("14. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 15:
            TestCode = get_model('lab_test_code', 'TestCode')
            in_destination = TestCode.objects.using(self.get_using_destination()).all().count()
            in_source = TestCode.objects.using(self.get_using_source()).all().count()
            print "15. checking TestCode. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("15. checking TestCode. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 16:
            AliquotType = get_model('lab_aliquot_list', 'AliquotType')
            in_destination = AliquotType.objects.using(self.get_using_destination()).all().count()
            in_source = AliquotType.objects.using(self.get_using_source()).all().count()
            print "17. checking AliquotType. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("17. checking AliquotType. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 18:
            for model in get_models(get_app('lab_panel')):
                in_destination = model.objects.using(self.get_using_destination()).all().count()
                in_source = model.objects.using(self.get_using_source()).all().count()
                print "18.{0} checking {1}. {2} objects in destination, {3} objects in source.".format(count, model.__name__, in_destination, in_source)
                # logger.info("18. checking {0}. {1} objects in destination, {2} objects in source.".format(in_destination, in_source, model.__name__))
                count += 1
            count = 0
        if not step > 19:
            AliquotType = get_model('lab_clinic_api', 'AliquotType')
            in_destination = AliquotType.objects.using(self.get_using_destination()).all().count()
            in_source = AliquotType.objects.using(self.get_using_source()).all().count()
            print "19. checking AliquotType. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("19. checking AliquotType. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 20:
            TestCodeGroup = get_model('lab_clinic_api', 'TestCodeGroup')
            in_destination = TestCodeGroup.objects.using(self.get_using_destination()).all().count()
            in_source = TestCodeGroup.objects.using(self.get_using_source()).all().count()
            print "20. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("20. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 21:
            TestCode = get_model('lab_clinic_api', 'TestCode')
            in_destination = TestCode.objects.using(self.get_using_destination()).all().count()
            in_source = TestCode.objects.using(self.get_using_source()).all().count()
            print "21. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("21. checking TestCodeGroup. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 22:
            Panel = get_model('lab_clinic_api', 'Panel')
            in_destination = Panel.objects.using(self.get_using_destination()).all().count()
            in_source = Panel.objects.using(self.get_using_source()).all().count()
            print "22. checking Panel. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("22. checking Panel. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 23:
            Review = get_model('lab_clinic_api', 'Review')
            in_destination = Review.objects.using(self.get_using_destination()).all().count()
            in_source = Review.objects.using(self.get_using_source()).all().count()
            print "23. checking Review. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("23. checking Review. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 24:
            UnscheduledLabEntryBucket = get_model('lab_entry', 'UnscheduledLabEntryBucket')
            in_destination = UnscheduledLabEntryBucket.objects.using(self.get_using_destination()).all().count()
            in_source = UnscheduledLabEntryBucket.objects.using(self.get_using_source()).all().count()
            print "24. checking UnscheduledLabEntryBucket. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("24. checking UnscheduledLabEntryBucket. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 25:
            LabEntry = get_model('lab_entry', 'LabEntry')
            in_destination = LabEntry.objects.using(self.get_using_destination()).all().count()
            in_source = LabEntry.objects.using(self.get_using_source()).all().count()
            print "25. checking LabEntry. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("25. checking LabEntry. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        if not step > 26:
            entry = get_model('entry', 'entry')
            in_destination = entry.objects.using(self.get_using_destination()).all().count()
            in_source = entry.objects.using(self.get_using_source()).all().count()
            print "26. checking Entry. {0} objects in destination, {1} objects in source.".format(in_destination, in_source)
            # logger.info("26. checking LabEntry. {0} objects in destination, {1} objects in source.".format(in_destination, in_source))
        logger.info("Done")
        print 'Done'
        # logger.setLevel(logging.WARNING)

    def backup_database(self, **kwargs):
        """Takes a backup of the netbook before preparing a netbook for dispatch"""
        # Check if were on the server or netbook
        fname = None
        if not settings.DEVICE_ID == self.server_device_id:
            raise TypeError('DB Snapshot must be done from the server.')
        if self._get_db_engine() == 'mysql':
            fname = self._backup_mysql_database()
        if self._get_db_engine() == 'sqlite3':
            fname = self._backup_sqlite3_database()
        if not fname:
            raise self.exception("DB Snapshot failed, unable to backup {0} database for {1}.".format(self._get_db_engine(), self.get_using_destination()))
        return fname

    def _backup_sqlite3_database(self):
        db = "{0}.db".format(self.get_using_destination())
        fd = self._get_backup_file_handle()
        con = sqlite3.connect("{0}.db".format(db))
        for row in con.execute('PRAGMA database_list;'):
            command_list = ['sqlite3', row[2], '.dump']
            if subprocess.Popen(command_list, stdout=fd).returncode:
                raise BackupError('Unable to backup. Tried with {0}'.format(command_list))
        return fd.name

    def _backup_mysql_database(self):
        db_user = settings.DATABASES[self.get_using_destination()]['USER']
        db_pass = settings.DATABASES[self.get_using_destination()]['PASSWORD']
        db = settings.DATABASES[self.get_using_destination()]['NAME']
        fd = self._get_backup_file_handle()
        command_list = ['mysqldump', '-u', db_user, '-p{0}'.format(db_pass), db]
        if subprocess.Popen(command_list, stdout=fd).returncode:
            raise BackupError('Unable to backup. Tried with {0}'.format(command_list))
        return fd.name

    def _restore_sqlite3_database(self):
        db = "{0}.db".format(self.get_using_destination())
        fd = open(self._get_last_backup_filename(), 'wb')
        con = sqlite3.connect("{0}.db".format(db))
        for row in con.execute('PRAGMA database_list;'):
            command_list = ['sqlite3', fd.name, '.restore']
            if subprocess.Popen(command_list, stdin=fd).returncode:
                raise BackupError('Unable to restore. Tried with {0}'.format(command_list))
        return fd.name

    def _restore_mysql_database(self, destination_host=None):
        db_user = settings.DATABASES[self.get_using_destination()]['USER']
        db_pass = settings.DATABASES[self.get_using_destination()]['PASSWORD']
        db = settings.DATABASES[self.get_using_destination()]['NAME']
        if not destination_host:
            destination_host = settings.DATABASES[self.get_using_destination()]['HOST']
        fd = self._get_backup_file_handle()
        command_list = ['mysql', '-h', destination_host, '-u', db_user, '-p{0}'.format(db_pass), db]
        if subprocess.Popen(command_list, stdin=fd).returncode:
            raise BackupError('Unable to restore. Tried with {0}'.format(command_list))
        return fd.name

    def _get_backup_file_handle(self):
        return open(self._get_next_backup_filename(), 'wb')

    def _get_next_backup_filename(self):
        return os.path.join(self._get_backup_path(), '{0}-{1}.sql'.format(self.get_using_destination(), datetime.today().strftime('%Y%m%d%H%M%S%f')))

    def _get_backup_path(self):
        """Returns the full path to the backup folder."""
        if not 'DB_SNAPSHOT_DIR' in dir(settings):
            backup_path = os.path.join(settings.DIRNAME, 'db_snapshots')
            if not os.path.exists(backup_path):
                subprocess.call(["mkdir", "-p", backup_path])
        else:
            backup_path = settings.DB_SNAPSHOT_DIR
            if not os.path.exists(backup_path):
                subprocess.call(["mkdir", "-p", backup_path])
        return backup_path

    def _get_db_engine(self):
        """Returns the database engine in use."""
        engine = settings.DATABASES[self.get_using_destination()]['ENGINE'].split('.')[-1:][0]
        if engine not in ['mysql', 'sqlite3']:
            raise TypeError('Unknown db engine. Got {0}'.format(engine))
        return engine

    def _get_last_backup_filename(self):
        """Returns the filename of the last backup for this destination."""
        last_filename = None
        # get list of files in backup path
        filenames = os.listdir(self._get_backup_path())
        if filenames:
            # remove any not starting in "destination"
            filenames = [filename for filename in filenames if filename.startswith(self.get_using_destination()) and filename.endswith('sql')]
            # if any items left, sort and pick the last one
            if filenames:
                filenames.sort()
                last_filename = os.path.join(self._get_backup_path(), filenames[-1:][0])
        return last_filename

    def restore_database(self, destination_host=None):
        """Loads previous database snapshot from disk."""
        fname = None
        if not settings.DEVICE_ID == self.server_device_id:
            raise TypeError('DB restore must be done from the server.')
        if self._get_db_engine() == 'mysql':
            fname = self._restore_mysql_database()
        if self._get_db_engine() == 'sqlite3':
            fname = self._restore_sqlite3_database()
        if not fname:
            raise RestoreError("Restore failed, unable to backup {0} database for {1}.".format(self._get_db_engine(), self.get_using_destination()))
        return fname
