from django.test import TestCase
from ..classes import site_mappers
from ..classes import Controller
from ..exceptions import MapperError


class ControllerTests(TestCase):
    
    

    def test_controller_methods(self):
        site_mappers.autodiscover()
        #Test 
        self.assertRaises(MapperError, site_mappers.get_current_mapper().map_area)