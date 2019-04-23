import logging
import json
import tempfile

from pywps import LiteralInput, ComplexInput
from pywps import ComplexOutput
from pywps import Process, FORMATS
from pywps.app.Common import Metadata
from owslib.wcs import WebCoverageService
from rasterstats import zonal_stats
from rasterio import MemoryFile
from raven.utils import archive_sniffer, crs_sniffer, single_file_check
from raven.utilities import gis


LOGGER = logging.getLogger("PYWPS")


class ZonalStatisticsProcess(Process):
    """Given files containing vector data and raster data, perform zonal statistics of the overlapping regions"""

    def __init__(self):
        inputs = [
            ComplexInput('shape', 'Vector Shape',
                         abstract='An ESRI Shapefile, GML, JSON, GeoJSON, or single layer GeoPackage.'
                                  ' The ESRI Shapefile must be zipped and contain the .shp, .shx, and .dbf.'
                                  ' The shape and raster should have a matching CRS.',
                         min_occurs=1, max_occurs=1,
                         supported_formats=[FORMATS.GEOJSON, FORMATS.GML, FORMATS.JSON, FORMATS.SHP]),
            # TODO: Update the metadata to reflect the EarthEnv DEM90 data source
            ComplexInput('raster', 'Gridded raster data set',
                         abstract='The DEM to be queried. Defaults to the USGS HydroSHEDS DEM.',
                         metadata=[Metadata('HydroSheds Database', 'http://hydrosheds.org'),
                                   Metadata(
                                       'Lehner, B., Verdin, K., Jarvis, A. (2008): New global hydrography derived from'
                                       ' spaceborne elevation data. Eos, Transactions, AGU, 89(10): 93-94.',
                                       'https://doi.org/10.1029/2008EO100001')],
                         min_occurs=0, max_occurs=1, supported_formats=[FORMATS.GEOTIFF],
                         ),
            LiteralInput('band', 'Raster band',
                         data_type='integer', default=1,
                         abstract='Band of raster examined to perform zonal statistics. Default: 1',
                         min_occurs=1, max_occurs=1),
            LiteralInput('return_geojson', 'Return the geometry and statistics as properties in a GeoJSON',
                         data_type='boolean', default='true',
                         min_occurs=1, max_occurs=1),
            LiteralInput('categorical', 'Return distinct pixel categories',
                         data_type='boolean', default='false',
                         min_occurs=1, max_occurs=1),
            LiteralInput('select_all_touching', 'Additionally select boundary pixels that are touched by shape',
                         data_type='boolean', default='false',
                         min_occurs=1, max_occurs=1),
            LiteralInput('WCS_VERSION', 'DEBUG FIELD SPECIFYING WCS VERSION USED TO ACCESS DEM',
                         data_type='string', default='1.0.0',
                         min_occurs=1, max_occurs=1)
        ]

        outputs = [
            ComplexOutput('statistics', 'DEM properties within the region defined by `shape`.',
                          abstract='Elevation statistics: min, max, mean, median, sum, nodata',
                          supported_formats=[FORMATS.JSON, FORMATS.GEOJSON]),
        ]

        super(ZonalStatisticsProcess, self).__init__(
            self._handler,
            identifier="zonal-stats",
            title="Raster Zonal Statistics",
            version="1.0",
            abstract="Return zonal statistics based on the boundaries of a vector file.",
            metadata=[],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):

        shape_url = request.inputs['shape'][0].file

        band = request.inputs['band'][0].data
        geojson_out = request.inputs['return_geojson'][0].data
        categorical = request.inputs['categorical'][0].data
        touches = request.inputs['select_all_touching'][0].data

        WCS_VERSION = request.inputs['WCS_VERSION'][0].data

        vectors = ['.gml', '.shp', '.gpkg', '.geojson', '.json']
        vector_file = single_file_check(archive_sniffer(shape_url, working_dir=self.workdir, extensions=vectors))
        rasters = ['.tiff', '.tif']

        if 'raster' in request.inputs:
            raster_url = request.inputs['raster'][0].file
            raster_file = single_file_check(archive_sniffer(raster_url, working_dir=self.workdir, extensions=rasters))
        else:
            bbox = gis.get_bbox(vector_file)
            raster_url = 'public__EarthEnv_DEM90_NorthAmerica'
            raster_file = MemoryFile(gis.get_dem(bbox, wcs_version=WCS_VERSION)).name

        vec_crs = crs_sniffer(vector_file)
        ras_crs = crs_sniffer(raster_file)

        if ras_crs != vec_crs:
            msg = 'CRS for files {} and {} are not the same.'.format(vector_file, raster_file)
            LOGGER.warning(msg)

        try:
            stats = zonal_stats(
                vector_file, raster_file, stats=['count', 'min', 'max', 'mean', 'median', 'sum', 'nodata'],
                band=band, categorical=categorical, all_touched=touches, geojson_out=geojson_out, raster_out=False)

            if not geojson_out:
                response.outputs['statistics'].data = json.dumps(stats)

            else:
                if len(stats) > 1:
                    feature_collect = {'type': 'FeatureCollection', 'features': stats}
                else:
                    feature_collect = stats

                response.outputs['statistics'].data = json.dumps(feature_collect)

                # import tempfile
                # thing = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False).name
                # with open(thing, 'w') as t:
                #     json.dump(feature_collect, t)

        except Exception as e:
            msg = 'Failed to perform zonal statistics using {} and {}: {}'.format(shape_url, raster_url, e)
            LOGGER.error(msg)
            raise Exception(msg)

        return response
