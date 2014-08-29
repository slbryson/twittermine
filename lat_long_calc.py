import pygmaps, pyproj, math


def get_utm_zone_number(longitude):
	return (int((longitude + 180)/6.0) % 60)


class zone_utm_longlat:
	def __init__(self, sw_longlat_tuple, ne_longlat_tuple, grid_length_mtrs):
		self.sw_longlat_tuple = sw_longlat_tuple
		self.ne_longlat_tuple = ne_longlat_tuple
		self.utm_zone = get_utm_zone_number(sw_longlat_tuple[0])
		self.geo_proj = pyproj.Proj(proj = 'utm', zone = self.utm_zone, ellps = 'WGS84')
		self.min_utm_cood_tuple = list(self.geo_proj(sw_longlat_tuple[0], sw_longlat_tuple[1]))
		self.grid_length_mtrs = grid_length_mtrs
		sw_grid_long, sw_grid_lat = self.geo_proj(self.min_utm_cood_tuple[0] + grid_length_mtrs,
													self.min_utm_cood_tuple[1] + grid_length_mtrs, 
													inverse = True)
		self.grid_length_long = sw_grid_long - sw_longlat_tuple[0]
		self.grid_length_lat = sw_grid_lat - sw_longlat_tuple[1]
		return


	def convert_latlong_to_utm(self, query_longlat_tuple):
		x_cood, y_cood = self.geo_proj(query_longlat_tuple[0], query_longlat_tuple[1])
		return x_cood, y_cood


	def convert_utm_to_longlat(self, query_utm_cood_tuple):
		longitude, latitude = self.geo_proj(query_utm_cood_tuple[0], 
											query_utm_cood_tuple[1], inverse = True)
		return longitude, latitude


	def get_grid_index(self, query_longlat_tuple):
		x_index = int((query_longlat_tuple[0] - self.sw_longlat_tuple[0])/(1.0 * self.grid_length_long))
		y_index = int((query_longlat_tuple[1] - self.sw_longlat_tuple[1])/(1.0 * self.grid_length_lat))
		return x_index, y_index


	def is_longlat_in_area(self, query_longlat_cood_tuple):
		if ((self.sw_longlat_tuple[0] <= query_longlat_cood_tuple[0] <= self.ne_longlat_tuple[0])
			and (self.sw_longlat_tuple[1] <= query_longlat_cood_tuple[1] <= self.ne_longlat_tuple[1])):
			return 1
		else:
			return 0


