import base64
import os
from io import BytesIO

import numpy as np

try:
    from PIL import Image
except ImportError:
    os.system('pip install pillow')
finally:
    from PIL import Image
    from PIL.ExifTags import TAGS

try:
    import requests
except ImportError:
    os.system('pip install requests')
finally:
    import requests


# Fetching Image From Given URL
# And Returning it as numpy array.
def url_to_img(url):
    img = Image.open(BytesIO(requests.get(url).content))
    exif_data = img.getexif()
    if exif_data is not None:
        orientation = exif_data.get(274)
        if orientation != 0:
            if orientation == 1:
                pass  # No rotation needed
            elif orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90)
            elif orientation == 7:
                img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90)
    return np.array(img)


# Fetching Image From Given base64 encoded
# And Returning it as numpy array.
def base64_to_img(base64_image):
    encoded_data = base64_image.split(",")[1]
    base64_decoded = base64.b64decode(encoded_data)
    image = Image.open(BytesIO(base64_decoded))
    return np.array(image)
