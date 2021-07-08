from PIL import Image
from os import listdir
import os

for file in listdir(f"images/tarot/Cups"):
     size = len(str(file))
     newName = (str(file)[:size - 4])
     im = Image.open(f"images/tarot/Cups/{file}")
     im = im.rotate(180, expand=True)
     im.save(f'images/tarot/Cups/{newName}-r.png')

# suit = 'Wands'
# location = ""
# for x in range(1,15,1):
#     print()
#     os.rename(f"images/tarot/{suit}/{suit}{str(x).zfill(2)}.png", f"images/tarot/{suit}/{str(x).zfill(2)}.png")
#     os.rename(f"images/tarot/{suit}/reversed-{suit}{str(x).zfill(2)}.png", f"images/tarot/{suit}/{str(x).zfill(2)}-r.png")

