import sys
import json
import socket

from django.core import serializers
from django.db import connection
from django.db.models import ForeignKey
from django.db.utils import IntegrityError

from edc.core.crypto_fields.classes import FieldCryptor

from .transaction_producer import TransactionProducer


class DeserializeFromTransaction(object):

    def deserialize_json_file(self, file_pointer):
        try:
            json_txt = file_pointer.read()
            decoded = json.loads(json_txt)
        except:
            return None
        return decoded

    def decrypt_transanction(self, incoming_transaction):
            model_dict = FieldCryptor('aes', 'local').decrypt(incoming_transaction.tx)
            return json.loads(model_dict)

    def deserialize(self, incoming_transaction, using, **kwargs):
        # may bypass this check for for testing ...
        using = using or 'default'
        check_hostname = kwargs.get('check_hostname', True)
        is_success = False
        tr = FieldCryptor('aes', 'local').decrypt(incoming_transaction.tx)

        for obj in serializers.deserialize("json", tr):
            # if you get an error deserializing a datetime, confirm dev version of json.py
            if incoming_transaction.action == 'D':
                #If the transactions is a DELETE then let the model itself deal with how
                #it handles this action by overiding method deserialize_prep() in the model.
                obj.object.deserialize_prep(action='D')
                incoming_transaction.is_ignored = False
                incoming_transaction.is_consumed = True
                incoming_transaction.consumer = str(TransactionProducer())
                incoming_transaction.save(using=using)
                is_success = True
            elif incoming_transaction.action == 'I' or incoming_transaction.action == 'U':
                # check if tx originanted from me
                # print "created %s : modified %s" % (obj.object.hostname_created, obj.object.hostname_modified)
                incoming_transaction.is_ignored = False
                print '    {0}'.format(obj.object._meta.object_name)
                if obj.object.hostname_modified == socket.gethostname() and check_hostname:
                    # ignore your own transactions
                    print '    skipping - not consuming my own transactions'.format(using)
                    is_success = False
                else:
                    is_success = False
                    # save using ModelBase save() method (skips all the subclassed save() methods)
                    # post_save, etc signals will fire
                    try:
                        obj.object.deserialize_prep()
                    except AttributeError:
                        pass
                    try:
                        # force insert even if it is an update
                        # to trigger an integrity error if it is an update
                        obj.save(using=using)
                        obj.object._deserialize_post(incoming_transaction)
                        print '    OK - normal save on {0}'.format(using)
                        is_success = True
                    except IntegrityError as error:
                        if 'Cannot add or update a child row' in error.args[1]:  # is this style deprecated?
                            # which foreign key is failing?
                            if 'audit' in obj.object._meta.db_table:
                                # audit tables do not have access to the helper methods
                                # for field in foreign_key_error:
                                #    # it is OK to just set the fk to None
                                #    setattr(obj.object, field.name, None)
                                print '    audit instance, ignoring... on using={0}'.format(using)
                                incoming_transaction.is_ignored = True
                            else:
                                foreign_key_error = []
                                for field in obj.object._meta.fields:
                                    if isinstance(field, ForeignKey):
                                        try:
                                            getattr(obj.object, field.name)
                                        except:
                                            print '    unable to getattr {0}'.format(field.name)
                                            foreign_key_error.append(field)
                                for field in foreign_key_error:
                                    print '    deserialize_get_missing_fk on model {0} for field {1} on using={2}'.format(obj.object._meta.object_name, field.name, using)
                                    setattr(obj.object, field.name, obj.object.deserialize_get_missing_fk(field.name))
                                try:
                                    obj.save(using=using)
                                    obj.object._deserialize_post(incoming_transaction)
                                    print '   OK saved after integrity error on using={0}'.format(using)
                                    is_success = True
                                except:
                                    incoming_transaction.is_ignored = True
                        elif 'Duplicate' in error.args[1]:
                            # if the integrity error refers to a duplicate
                            # check the unique_together meta class value to attempt to
                            # locate the existing pk.
                            # If pk found, overwrite the pk in the json with the existing pk.
                            # Try to save again
                            print '    duplicate on {0}'.format(using)
                            if not obj.object._meta.unique_together:
                                # if there is no other constraint on the model
                                # then an integrity error does not really make sense.
                                # but anyway ...
                                print '   missing unique_together attribute'
                                raise
                            options = {}
                            for tpl in obj.object._meta.unique_together:
                                for f in tpl:
                                    options.update({f: getattr(obj.object, f)})
                                if not obj.object.__class__.objects.filter(**options).exists():
                                    # it should exist, otherwise how did we get an integrity error?
                                    print '   not found using unique_together field atttributes'
                                    raise
                                else:
                                    old_pk = obj.object.id
                                    new_pk = obj.object.__class__.objects.get(**options).pk
                                    obj.object.id = new_pk
                                    try:
                                        print '    deserialize_on_duplicate'
                                        if 'deserialize_on_duplicate' in dir(obj.object) and obj.object.deserialize_on_duplicate():
                                            print '    deserialize_on_duplicate'
                                            # obj.object.deserialize_on_duplicate()
                                            # not every duplicate needs to be saved
                                            # if you can develop criteria to decide,
                                            # then use deserialize_on_duplicate to evaluate
                                            print '    try save again'
                                            obj.save(using=using)
                                            obj.object._deserialize_post(incoming_transaction)
                                            is_success = True
                                            # change all pk to the new pk for is_consumed=False.
                                            print '    OK saved, now replace_pk_in_tx on using={0}'.format(using)
                                            incoming_transaction.__class__.objects.replace_pk_in_tx(old_pk, new_pk, using)
                                            print '    {0} is now {1}'.format(old_pk, new_pk)
                                        else:
                                            print '    no deserialize_on_duplicate method/model choosing to ignore duplicate'
                                            incoming_transaction.is_ignored = True
                                            incoming_transaction.is_error = True
                                            incoming_transaction.save(using=using)
                                    except IntegrityError as error:
                                        print '    integrity error ... giving up.'
                                        incoming_transaction.is_consumed = False
                                        incoming_transaction.consumer = None
                                        incoming_transaction.is_error = True
                                        incoming_transaction.error = error
                                        incoming_transaction.save(using=using)
                                    except:
                                        print "        [a] Unexpected error:", sys.exc_info()[0]
                                        raise
                        else:
                            print '    {0}'.format(error)
                            raise
                    except:
                        print connection.queries
                        print "        [b] Unexpected error:", sys.exc_info()
                        raise
                    if is_success:
                        incoming_transaction.is_consumed = True
                        incoming_transaction.consumer = str(TransactionProducer())
                        incoming_transaction.save(using=using)
        return is_success
