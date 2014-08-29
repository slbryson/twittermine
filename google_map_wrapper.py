import urllib, json, urllib

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_bounding_box_longlats(address): 
	url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
	uh = urllib.urlopen(url)
	data = uh.read()
	js = json.loads(str(data))
	bounds = js['results'][0]['geometry']['bounds']
	sw_longlat_tuple = [bounds['southwest']['lng'], bounds['southwest']['lat']]
	ne_longlat_tuple = [bounds['northeast']['lng'], bounds['northeast']['lat']]
	bbox_coods = [sw_longlat_tuple[0], sw_longlat_tuple[1], ne_longlat_tuple[0], ne_longlat_tuple[1]]
	bbox_strng = ','.join([str(x) for x in bbox_coods])
	return sw_longlat_tuple, ne_longlat_tuple, bbox_strng



