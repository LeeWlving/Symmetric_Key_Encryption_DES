from PIL import Image
import io
import json,requests,base64
img="4.1.04.tiff"

with open(img, "rb") as imageFile:
    image2str = base64.b64encode(imageFile.read())
    print(image2str)
with open('text.txt',"w+") as f:
    f.write(str(image2str))
