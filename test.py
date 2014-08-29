import TwitterAPI
import urllib, json

CK = 'YyxjZoC9JRIF2Ynlrdbi5sH9l'
CS = 'jFH6tuBHKaV6B0Am5cGCJpydZiYbSnuz6hqPlZZMSnzvM9jOF1'
AT = '2742390818-BYNy3F2ONHVe85nTby7UVm3JPuOn4DaGef2swip'
ATS = 'vicUnQoWftfkLhCW7wsJV1oNmmCAQG3j1EDvIuh3ss6GQ'
api = TwitterAPI.TwitterAPI(CK, CS, AT, ATS)
r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
for item in r.get_iterator():
    print item

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
import json
import urllib
address = 'Phoenix, AZ'
url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
uh = urllib.urlopen(url)
data = uh.read()
js = json.loads(str(data))

sw_lat = js['results'][0]['geometry']['bounds']['southwest']['lat']
sw_lng = js['results'][0]['geometry']['bounds']['southwest']['lng']
ne_lat = js['results'][0]['geometry']['bounds']['northeast']['lat']
ne_lng = js['results'][0]['geometry']['bounds']['northeast']['lng']
bbox_coods = [sw_lng, sw_lat, ne_lng, ne_lat]
bbox_strng = ','.join([str(x) for x in bbox_coods])

r = api.request('statuses/filter', {'locations': bbox_strng})
count = 0
tws = []
for item in r.get_iterator():
    tws.append(item['geo']['coordinates'])
    count = count + 1
    if count == 20:
        break


