from django.db import models
from audit.audit_trail import AuditTrail
from base.model.models import BaseListModel
from testing.models import TestM2m
from device.dispatch.models import BaseDispatchSyncUuidModel


class TestDspList(BaseListModel):
    class Meta:
        app_label = 'testing'


class TestDspContainer(BaseDispatchSyncUuidModel):

    test_container_identifier = models.CharField(max_length=35, unique=True)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_container_identifier

    def dispatched_as_container_identifier_attr(self, using=None):
        return 'test_container_identifier'

    def is_dispatch_container_model(self):
        return True

    def dispatch_container_lookup(self):
        return None

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'


class TestDspItem(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestDspContainer)

    test_m2m = models.ManyToManyField(TestM2m)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (TestDspContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'


class TestDspItemTwo(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item = models.ForeignKey(TestDspItem)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'


class TestDspItemThree(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_two = models.ForeignKey(TestDspItemTwo)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item_two__test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'


class TestDspItemM2M(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_three = models.ForeignKey(TestDspItemThree)

    m2m = models.ManyToManyField(TestDspList)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item_two__test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'


class TestDspItemBypass(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestDspContainer)

    test_m2m = models.ManyToManyField(TestM2m)

    f1 = models.CharField(max_length=35)
    f2 = models.CharField(max_length=35)
    f3 = models.CharField(max_length=35)
    f4 = models.CharField(max_length=35)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def bypass_for_edit_dispatched_as_item(self):
        # requery myself
        obj = self.__class__.objects.get(pk=self.pk)
        #dont allow values in these fields to change if dispatched (means only f1, f2 can change)
        may_not_change = [(k, v) for k, v in obj.__dict__.iteritems() if k not in ['f1', 'f2']]
        for k, v in may_not_change:
            if k[0] != '_':
                if getattr(self, k) != v:
                    print 'cannot bypass, failed on field {0}'.format(k)
                    return False
        return True

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (TestDspContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'testing'
