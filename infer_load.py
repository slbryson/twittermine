import ConfigParser, sys
import lat_long_calc as llc
import google_map_wrapper as gmw
import twitter_api_wrapper as taw
from save_data import *

CONFIG_FILENAME = 'load_inference_config.ini'

def get_location_info(config_filename):
	cfg = ConfigParser.ConfigParser()
	cfg.read(config_filename)
	city = cfg.get('LOCATION', 'CITY')
	state = cfg.get('LOCATION', 'STATE')
	address = ",".join([city, state])
	grid_length_mtrs = cfg.getfloat('LOCATION', 'GRID_LENGTH_IN_MTR')
	return address, grid_length_mtrs



def main(duration_minutes, reset_db):
	#First get the location information by calling the CONFIG PARSER
	address, grid_length_mtrs = get_location_info(CONFIG_FILENAME)
	print 'Address =', address, "  ", grid_length_mtrs
	#Use the Google serers to calculate the bounding box
	sw_longlat, ne_longlat, bbox_strng = gmw.get_bounding_box_longlats(address)
	print "SW long lat =", sw_longlat, 'NE long lat =', ne_longlat
	#Develop the Zone information
	zone = llc.zone_utm_longlat(sw_longlat, ne_longlat, grid_length_mtrs)
	# Only call count_tweets
	tweet_count_dict = taw.count_tweets(bbox_strng, zone, duration_minutes, reset_db)
	# The json file may just be an alternate format
	#write_as_json(tweet_count_dict)
	
	return tweet_count_dict


if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print 'Enter duration of counting in minutes, Restart counting (0=No/1=Yes)?'
	else:
		main(int(sys.argv[1]), int(sys.argv[2]))

	


