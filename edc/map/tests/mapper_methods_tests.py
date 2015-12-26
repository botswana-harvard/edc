from django.db import models
from django.test import TestCase

from ..classes import site_mappers
from ..classes import Mapper
from ..exceptions import MapperError


class TestPlot(models.Model):

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text="Plot identifier",
        editable=False,
        db_index=True)

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        editable=False)

    gps_degrees_s = models.DecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0)

    gps_minutes_s = models.DecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_degrees_e = models.DecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0)

    gps_minutes_e = models.DecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_lon = models.DecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_lat = models.DecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    class Meta:
        app_label = 'map'


class TestPlotMapper(Mapper):
    map_area = 'test_community'
    map_code = '999'
    identifier_field_attr = 'plot_identifier'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.011111
    gps_center_lon = 25.741111
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class MapperTests(TestCase):

    def test_mapper_methods(self):
        site_mappers.autodiscover()
        mapper = site_mappers.get_registry('test_community')()
        lat = None
        lon = None
        plot = TestPlot.objects.create(
            community='test_community',
            gps_target_lon=25.745569,
            gps_target_lat=-25.032927)

        items = [plot]

        # Test gps_distance_between_points(self, lat, lon, center_lat=None, center_lon=None, radius=None): method
        self.assertRaises(
            MapperError, mapper.gps_distance_between_points, lat, lon)
        self.assertEqual(
            mapper.gps_distance_between_points(-24.656637, 25.924327, -24.656366, 25.922935),
            0.14407256837110122, 'Correct distance if matching')
        # Test deg_to_dm(dd) method
        self.assertEqual(
            mapper.deg_to_dm(-24.656637), [24.0, 39.39822000000004],
            'converted to this: -24.656637 to this : 24.0, 39.39822000000004]')
        # Test get_cardinal_point_direction(self, start_lat, start_lon, end_lat, end_lon) method
        self.assertEqual(mapper.get_cardinal_point_direction(-24.656637, 25.924327, -24.656366, 25.922935), (0.144, 'W'), 'Direction and distance between two point')
        # Test verify_gps_to_target(self, lat, lon, center_lat, center_lon, radius, exception_cls)
        self.assertEqual(
            mapper.verify_gps_to_target(-24.656637, 25.924327, -24.656637, 25.924327, 0.025, MapperError),
            True, 'The is the same point targeted')
        self.assertEqual(
            mapper.prepare_map_points(
                items, selected_icon='', cart='', cart_icon='egg-circle.png',
                dipatched_icon='red-circle.png', selected_section="All",
                selected_sub_section='ALL'),
            [25.745569, -25.032927, getattr(items[0], mapper.identifier_field_attr), 'blue-circle.png', ''])
