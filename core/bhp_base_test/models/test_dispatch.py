from django.db import models
from edc.audit.audit_trail import AuditTrail
from edc.base.model.models import BaseListModel
from edc.core.bhp_base_test.models import TestManyToMany
from edc.core.bhp_dispatch.models import BaseDispatchSyncUuidModel


class TestDispatchList(BaseListModel):
    class Meta:
        app_label = 'bhp_base_test'


class TestDispatchContainer(BaseDispatchSyncUuidModel):

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
        app_label = 'bhp_base_test'


class TestDispatchItem(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestDispatchContainer)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (TestDispatchContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_base_test'


class TestDispatchItemTwo(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item = models.ForeignKey(TestDispatchItem)

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
        app_label = 'bhp_base_test'


class TestDispatchItemThree(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_two = models.ForeignKey(TestDispatchItemTwo)

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
        app_label = 'bhp_base_test'


class TestDispatchItemM2M(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_three = models.ForeignKey(TestDispatchItemThree)

    m2m = models.ManyToManyField(TestDispatchList)

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
        app_label = 'bhp_base_test'


class TestDispatchItemBypassForEdit(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestDispatchContainer)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

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
        return (TestDispatchContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_base_test'
