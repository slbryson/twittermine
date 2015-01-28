import TwitterAPI
import urllib, json
from lat_long_calc import *
from datetime import *
import numpy as np
from save_data  import *
import redis


CK = 'YyxjZoC9JRIF2Ynlrdbi5sH9l'
CS = 'jFH6tuBHKaV6B0Am5cGCJpydZiYbSnuz6hqPlZZMSnzvM9jOF1'
AT = '2742390818-BYNy3F2ONHVe85nTby7UVm3JPuOn4DaGef2swip'
ATS = 'vicUnQoWftfkLhCW7wsJV1oNmmCAQG3j1EDvIuh3ss6GQ'

TIME_CHECK_INTERVAL_ITERATIONS = 5
REDIS_SAVE_EVERY_N_TWEETS = 100


def count_tweets(bbox_strng, zone, duration_minutes, reset_db):
	grid_index_dict, tweet_count_dict = create_count_dict(zone)
	# r_server is the redis read dictionary.
	# tweet_count_dict is overall bounding box of the city broken into grids.  
	# This allows the counts to be located within one of the tile points an counted.  
	r_server  = initiate_redis_DB(tweet_count_dict, reset_db)

	api = TwitterAPI.TwitterAPI(CK, CS, AT, ATS)
	end_time = datetime.now() + timedelta(seconds = int(60 * duration_minutes))
	r = api.request('statuses/filter', {'locations': bbox_strng})
	tws =[]
	count = 0
	
	for item in r.get_iterator():
		if (count % TIME_CHECK_INTERVAL_ITERATIONS == 0):
			if (datetime.now() > end_time):
				break

		if item['coordinates']:
			#twt_loc is already our exact coordinates
			twt_loc = item['coordinates']['coordinates']
			# We also need id and created_at
			twt_id = item['id']
			twt_time = item['created_at']
			data = [twt_id, twt_loc[1], twt_loc[0], twt_time]
			tws.append(data)
			# We will keep this code, but really not necessary since the twitter API filter on locations will only return tweets from our desired location.  The code below simply pegs one of the sub grids that were created
			if (zone.is_longlat_in_area(twt_loc) == 1):
				i, j = zone.get_grid_index(twt_loc)
				grid_key = grid_index_dict[(i, j)]
				tweet_count_dict[grid_key] += 1
				#tweet_count dictionary is incremented is later used
				# to count.  However REDIS is updated with the statement
				# below @ grid_key.
				# We should add a key in the r_server dictionary based
				# on the id of the tweeter.
				# Ripping out the grid as a key and replacing with ids.
				#r_server.incr(list(grid_key))
				r_server.append(twt_id,[twt_loc,twt_time])
		count += 1
		if (count % REDIS_SAVE_EVERY_N_TWEETS == 0):
			r_server.save()

	r_server.save()
	# The module call to save from the redis dB to the CSV is temporarily removed.
	#save_redis_DB_to_csv(r_server)
	# Instead we use a simple write of the data to csv.  please don't let Supratim see this.  He will be disappointed.
	save_raw_to_csv(tws)
	return tweet_count_dict


#The below routine would create raw tweet counts
def save_tweets(bbox_strng, max_tweets):
	api = TwitterAPI.TwitterAPI(CK, CS, AT, ATS)
	r = api.request('statuses/filter', {'locations': bbox_strng})
	count = 0
	tws = []
	for item in r.get_iterator():
		if (item['coordinates']):
			twt_loc = item['coordinates']['coordinates']
			# We also need id and created_at
			twt_id = item['id']
			twt_time = item['created_at']
			data = [twt_id, twt_loc, twt_time]
			tws.append(data)
			# older write of just the coordinateds.
			#tws.append(item['coordinates']['coordinates'])
		count = count + 1
		if count == max_tweets:
			break
	return tws



def create_count_dict(zone):
	tweet_count_dict = {}
	grid_index_dict = {}
	x_index_max, y_index_max = zone.get_grid_index(zone.ne_longlat_tuple)
	for i in range(0, x_index_max + 1):
		for j in range(0, y_index_max + 1):
			sw_grid_point_longlat = (zone.sw_longlat_tuple[0] + i * zone.grid_length_long, zone.sw_longlat_tuple[1] + j * zone.grid_length_lat)
			mid_point_grid = (sw_grid_point_longlat[0] + 0.5 * zone.grid_length_long, sw_grid_point_longlat[1] + 0.5 * zone.grid_length_lat)
			grid_index_dict[(i, j)] = mid_point_grid
			tweet_count_dict[mid_point_grid] = 0

	return grid_index_dict, tweet_count_dict
