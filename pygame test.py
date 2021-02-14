from PIL import Image, ImageDraw
import numpy as np

img = Image.new('RGB', (100, 100))
drw = ImageDraw.Draw(img, 'RGBA')
drw.polygon([(0,0), (0,100), (100, 100), (100, 0)], (255, 255, 255, 255))
drw.polygon([(0, 0), (100, 0), (0, 100), (100,100)], (255, 0, 0, 128))
# drw.polygon([(50,100), (100, 0), (0, 0)], (0, 255, 0, 125))
del drw

# img.save('out.png', 'PNG')
img.show()

a= np.array(img).reshape(-1)
print(a)
