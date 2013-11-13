import mimetypes 
from django.http import HttpResponse, Http404
from django.conf import settings
from ..classes import site_mappers
from ..exceptions import MapperError
from database_storage import DatabaseStorage


def blog_attach(request, **kwargs):
    
    mapper_name = kwargs.get('mapper_name', '')
    mapper_item_label = kwargs.get('mapper_item_label', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        identifier = kwargs.get('identifier', None)
        item = mapper.get_item_model_cls().objects.get(**{mapper.get_identifier_field_attr(): identifier})
        if kwargs.get('map', None):
            map = int(kwargs.get('map', None)) 
            if map == 1:
                # Read file from database
                storage = DatabaseStorage(settings.DB_FILES)
                image_file = storage.open(item.uploaded_map_18.name, 'rb')
                if not image_file:
                    raise Http404
                file_content = image_file.read()
               
                # Prepare response
                content_type, content_encoding = mimetypes.guess_type(item.uploaded_map_18.name)
                response = HttpResponse(content=file_content, mimetype=content_type)
                response['Content-Disposition'] = 'inline; filename=%s' % item.uploaded_map_18.name
                if content_encoding:
                    response['Content-Encoding'] = content_encoding
                return response
                
                
            if map == 2:
                # Read file from database
                storage = DatabaseStorage(settings.DB_FILES)
                image_file = storage.open(item.uploaded_map_17.name, 'rb')
                if not image_file:
                    raise Http404
                file_content = image_file.read()
               
                # Prepare response
                content_type, content_encoding = mimetypes.guess_type(item.uploaded_map_17.name)
                response = HttpResponse(content=file_content, mimetype=content_type)
                response['Content-Disposition'] = 'inline; filename=%s' % item.uploaded_map_17.name
                if content_encoding:
                    response['Content-Encoding'] = content_encoding
                return response
            
            
            if map == 3:
                # Read file from database
                storage = DatabaseStorage(settings.DB_FILES)
                image_file = storage.open(item.uploaded_map_16.name, 'rb')
                if not image_file:
                    raise Http404
                file_content = image_file.read()
               
                # Prepare response
                content_type, content_encoding = mimetypes.guess_type(item.uploaded_map_16.name)
                response = HttpResponse(content=file_content, mimetype=content_type)
                response['Content-Disposition'] = 'inline; filename=%s' % item.uploaded_map_16.name
                if content_encoding:
                    response['Content-Encoding'] = content_encoding
                return response
        return response