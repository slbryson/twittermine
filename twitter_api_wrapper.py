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
	r_server = initiate_redis_DB(tweet_count_dict, reset_db)

	api = TwitterAPI.TwitterAPI(CK, CS, AT, ATS)
	end_time = datetime.now() + timedelta(seconds = int(60 * duration_minutes))
	r = api.request('statuses/filter', {'locations': bbox_strng})
	count = 0
	
	for item in r.get_iterator():
		if (count % TIME_CHECK_INTERVAL_ITERATIONS == 0):
			if (datetime.now() > end_time):
				break

		if item['coordinates']:
			twt_loc = item['coordinates']['coordinates']
			if (zone.is_longlat_in_area(twt_loc) == 1):
				i, j = zone.get_grid_index(twt_loc)
				grid_key = grid_index_dict[(i, j)]
				tweet_count_dict[grid_key] += 1
				r_server.incr(list(grid_key))
		count += 1
		if (count % REDIS_SAVE_EVERY_N_TWEETS == 0):
			r_server.save()

	r_server.save()
	save_redis_DB_to_csv(r_server)
	return tweet_count_dict



def save_tweets(bbox_strng, max_tweets):
	api = TwitterAPI.TwitterAPI(CK, CS, AT, ATS)
	r = api.request('statuses/filter', {'locations': bbox_strng})
	count = 0
	tws = []
	for item in r.get_iterator():
		if (item['coordinates']):
				tws.append(item['coordinates']['coordinates'])
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
