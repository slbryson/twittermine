

import json, redis, csv

OUTPUT_FILE = 'output.json'
OUTPUT_CSV = 'denver.csv'
REDIS_SERVER = "localhost"


def write_as_json(tweet_count_dict):
	json_compatible_dict = ([{'location' : k, 'tweet_count' : tweet_count_dict[k]}
							for k in tweet_count_dict.keys()])
	with open(OUTPUT_FILE, 'w') as fw:
		json.dump(json_compatible_dict, fw)


def initiate_redis_DB(tweet_count_dict, reset_db):
	r_server = redis.Redis(REDIS_SERVER)
	# note this code only gets executed if the user input is 1 for reset
	if (reset_db == 1):
		r_server.flushdb()
		# Remove the grid as a dictionary primer
		if false:
			for key in tweet_count_dict:
				r_server.set(list(key), 0)
	return r_server

def save_redis_DB_to_disk(r_server):
	r_server.save()
	return


def save_raw_to_csv(tws):
	with open(OUTPUT_CSV, 'w') as fp:
		w = csv.writer(fp, delimiter=',')
		data = [[ "User_id", "latitude", "longitude", "time_stamp"]]
		for key in tws:
			data.append(key)
		w.writerows(data)
	return


def save_redis_DB_to_csv(r_server):
	with open(OUTPUT_CSV, 'w') as fp:
		w = csv.writer(fp, delimiter=',')
		#data = [[ "latitude", "longitude", "tweet_count"]]
		# With the change in dictionary r_server will consist of uid, location, time
		# each key will be a user
		data = [[ "User_id", "latitude", "longitude", "time_stamp"]]
		for key in r_server.keys():
			#longlat will NOT be the key in my modified dbase the user_id is tehe key and lat/long/time are values
			#longlat = json.loads(key) 
			user_id = json.loads(key)
			#old count that only added to grid points that had values.  recall we initialized the database with the entire grid.
			if False:
				count = json.loads(r_server.get(key))
				if (count > 0):
					new_data = [longlat[1], longlat[0], count] 
					data.append(new_data)
			if True:
				longlat = json.loads(r_server.get(key))
				if (longlat >0):
					print 'longlat', longlat, ' type =', type(longlat)
					new_data = [user_id, longlat[1], longlat[0], longlat[2]]
					data.append(new_data)
		w.writerows(data)
		return
