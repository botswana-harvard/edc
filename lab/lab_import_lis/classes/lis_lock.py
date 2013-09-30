import logging
from edc.core.bhp_lock.classes import BaseLock
from ..models import LisLockModel, LisImportHistoryModel

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class LisLock(BaseLock):

    def __init__(self, db):
        self.db = db
        super(LisLock, self).__init__(db, LisLockModel, LisImportHistoryModel)
