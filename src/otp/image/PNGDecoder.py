import base64
from panda3d.core import StringStream, PNMImage

# Decode the image and load it into Panda
def decodeData(filename, data):
 b64image = data
 stream = StringStream(base64.b64decode(b64image))
 image = PNMImage()
 endname = filename + ".png"
 return image.read(stream, endname)

