# import urllib2
import urllib.request
import base64
import json

f = open("foo.png", "rb") # open our image file as read only in binary mode
image_data = f.read()              # read in our image file
b64_image = base64.standard_b64encode(image_data)

client_id = "5f4ec90a7daf0da" # put your client ID here
headers = {'Authorization': 'Client-ID ' + client_id}

data = {'image': b64_image, 'title': 'test'} # create a dictionary.

request = urllib.request.Request(url="https://api.imgur.com/3/upload.json", data=urllib.parse.urlencode(data).encode('utf-8'),headers=headers)
response = urllib.request.urlopen(request).read()

parse = json.loads(response)
print(parse['data']['link'])