import random

niceColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Get a random (but good looking) color
def getRandomColor():
  return niceColors[random.randrange(0, len(niceColors))]
