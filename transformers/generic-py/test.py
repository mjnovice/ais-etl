import requests
from PIL import Image
from io import BytesIO
from trans import ops
path="/test-bck/monkey"
r = requests.get("http://192.168.0.3:8080/v1/objects" + path)
img = r.content
print(type(img))
for op in ops:
    img = op(img)
print(img)
#img.convert("RGB").show()
