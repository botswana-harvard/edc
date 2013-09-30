# import sys,os
# sys.path.append('/home/django/source/')
# sys.path.append('/home/django/source/bhplab/')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'bhplab.settings'
# from django.core.management import setup_environ
# from bhplab import settings
# 
# setup_environ(settings)
# 
# from lab_import_dmis.classes import DmisOrder
# 
# 
# def fetch_order(**kwargs):
#     dmis_order = DmisOrder()
#     dmis_order.fetch_order(**kwargs)
# 
# if __name__ == "__main__":
#     print 'fetching lab orders from dmis....'
#     print 'fetching orders....'
#     if len(sys.argv) > 1:
#         fetch_order(subject_identifier=sys.argv[1], lab_db=sys.argv[2])
#     else:
#         fetch_order()
#     print 'Done'
#     sys.exit(0)
