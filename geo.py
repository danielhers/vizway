import pyproj


class ItmToWGS84(object):
    def __init__(self):
        # initializing WGS84 (epsg: 4326) and Israeli TM Grid (epsg: 2039) projections.
        # for more info: http://spatialreference.org/ref/epsg/<epsg_num>/
        self.wgs84 = pyproj.Proj(init='epsg:4326')
        self.itm = pyproj.Proj(init='epsg:2039')

    def convert(self, x, y):
        """
        converts ITM to WGS84 coordinates
        :type x: float
        :type y: float
        :rtype: tuple
        :return: (long,lat)
        """
        longitude, latitude = pyproj.transform(self.itm, self.wgs84, x, y)
        return longitude, latitude