

import json, redis, csv

OUTPUT_FILE = 'output.json'
OUTPUT_CSV = 'output.csv'
REDIS_SERVER = "localhost"


def write_as_json(tweet_count_dict):
	json_compatible_dict = ([{'location' : k, 'tweet_count' : tweet_count_dict[k]}
							for k in tweet_count_dict.keys()])
	with open(OUTPUT_FILE, 'w') as fw:
		json.dump(json_compatible_dict, fw)


def initiate_redis_DB(tweet_count_dict, reset_db):
	r_server = redis.Redis(REDIS_SERVER)
	if (reset_db == 1):
		r_server.flushdb()
		for key in tweet_count_dict:
			r_server.set(list(key), 0)
	return r_server

def save_redis_DB_to_disk(r_server):
	r_server.save()
	return


def save_redis_DB_to_csv(r_server):
	with open(OUTPUT_CSV, 'w') as fp:
		w = csv.writer(fp, delimiter=',')
		data = [[ "latitude", "longitude", "tweet_count"]]
		for key in r_server.keys():
			longlat = json.loads(key) 
			count = json.loads(r_server.get(key))
			if (count > 0):
				new_data = [longlat[1], longlat[0], count] 
				data.append(new_data)
		w.writerows(data)
		return