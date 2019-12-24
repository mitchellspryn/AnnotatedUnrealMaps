import airsim.airsim_types as at

class LocalizedPoint(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.vec = at.Vector3r(x_val=x, y_val=y, z_val=z)

        self.geo_point = None

    def location_xyz(self):
        return self.vec

    def location_geo(self):
        if (self.geo_point is None):
            raise ValueError('Attempting to get location_geo before calling set_geo() in AnnotatedPoi')

        return self.geo_point

    def set_geo(self, geo_point):
        self.geo_point = geo_point

        self.latitude = self.geo_point['latitude'],
        self.longitude = self.geo_point['longitude'],
        self.altitude = self.geo_point['altitude']

    def __add__(self, other):
        return at.Vector3r(x_val=self.x + other.x, y_val=self.y+other.y, z_val=self.z+other.z)

    def __sub__(self, other):
        return at.Vector3r(x_val=self.x - other.x, y_val=self.y-other.y, z_val=self.z-other.z)

    def __mul__(self, scalar):
        return at.Vector3r(x_val=self.x * scalar, y_val=self.y * scalar, z_val = self.z * scalar)
