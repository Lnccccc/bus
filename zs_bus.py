import requests
import time
import random
from PIL import Image
from io import BytesIO
def get_bus_info():
    user_agent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50']
    headers = {"user-agent" : "{}".format(random.choice(user_agent))}

    info = requests.get(url='http://113.106.3.65:4180/realtimebus/query/queryService/getLineInfoAndCardInfo?p0=886050&p1=2',
                        headers=headers)
    j_info = info.json()
    return j_info

location = []
alpha = 'ABCDEFGHIJK'
markers =''
markers2=''
markers3 = ''
raw_locations = ''
info = get_bus_info()
fuyi = str(info['line'][26]['lng'])+','+str(info['line'][26]['lat'])
print(fuyi)
for i in range(len(info['line'])):
    location.append('%s,%s|' % (info['line'][i]['lng'],info['line'][i]['lat']))
for i in range(len(location)):
    raw_locations += location[i]
locations_api = requests.get("https://restapi.amap.com/v3/assistant/coordinate/convert?locations="+raw_locations+"&coordsys=baidu&output=json&key=40aec8af51d4c65702feba24cf2e7aa7")
json_locations_api = locations_api.json()
location=json_locations_api['locations'].split(';')

for i in range(10):
    markers +=location[i]+';'
markers = 'A:'+markers
print(markers)
for i in range(10,20):
    markers3 +=location[i]+';'
markers3 = 'A:'+markers3
for i in range(20,30):
    markers2 +=location[i]+';'
markers2 = 'A:'+markers2



map_api = "https://restapi.amap.com/v3/staticmap?location="+fuyi+"&zoom=12&size=1024*1024&markers=mid,,"+markers[:-1]+"&key=40aec8af51d4c65702feba24cf2e7aa7"
map_api2 = "https://restapi.amap.com/v3/staticmap?location="+fuyi+"&zoom=12&size=1024*1024&markers=mid,,"+markers2[:-1]+"&key=40aec8af51d4c65702feba24cf2e7aa7"
map_api3 = "https://restapi.amap.com/v3/staticmap?location="+fuyi+"&zoom=12&size=1024*1024&markers=mid,,"+markers3[:-1]+"&key=40aec8af51d4c65702feba24cf2e7aa7"

bus_map = requests.get(url=map_api)
bus_map2 = requests.get(url=map_api2)
bus_map3 = requests.get(url=map_api3)

im1 = Image.open(BytesIO(bus_map.content))
im2 = Image.open(BytesIO(bus_map2.content))
im3 = Image.open(BytesIO(bus_map3.content))
im3 = im3.convert(mode='RGBA')
im2 = im2.convert(mode='RGBA')
im1 = im1.convert(mode='RGBA')
im4 = Image.blend(im1,im2,alpha=0.5)
im5 = Image.blend(im4,im3,alpha=0.5)
im5.show()