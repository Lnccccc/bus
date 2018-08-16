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
for i in range(len(info['line'])):
    location.append('%s,%s|' % (info['line'][i]['lng'],info['line'][i]['lat']))
for i in range(len(location)):
    raw_locations += location[i]
locations_api = requests.get("https://restapi.amap.com/v3/assistant/coordinate/convert?locations="+raw_locations+"&coordsys=baidu&output=json&key=40aec8af51d4c65702feba24cf2e7aa7")
json_locations_api = locations_api.json()
location=json_locations_api['locations'].split(';')

location_dic = {}
for i in range(10):
    markers +=location[i]+';'
location_dic.update({'market1': 'A:'+markers})
for i in range(10,20):
    markers3 +=location[i]+';'
location_dic.update({'market3':'A:'+markers3})
for i in range(20,30):
    markers2 +=location[i]+';'
location_dic.update({'market2' : 'A:'+markers2})
print(location_dic[list(location_dic.keys())[0]])
location_list = []
for i in range(len(location_dic.keys())):
    map_api = "https://restapi.amap.com/v3/staticmap?location="+fuyi+"&zoom=12&size=1024*1024&markers=mid,,"+location_dic[list(location_dic.keys())[i]][:-1]+"&key=40aec8af51d4c65702feba24cf2e7aa7"
    bus_map = requests.get(url=map_api)
    im1 = Image.open(BytesIO(bus_map.content))
    im1 = im1.convert(mode='RGBA')
    location_list.append(im1)
im4 = Image.blend(location_list[0],location_list[1],alpha=0.5)
im5 = Image.blend(location_list[2],im4,alpha=0.5)
im5.show()


##如何做一个更好的实时公交系统？