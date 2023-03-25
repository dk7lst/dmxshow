# Conrad OctoPod OP-75 RGB-LED-Spot
# uses 4 DMX channels
class OctoPod75:
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def clear(self):
    self.set(0, 0, 0)

  def set(self, r, g, b, flashSpeedPercent = 0):
    assert flashSpeedPercent >= 0 and flashSpeedPercent <= 100
    self.dmx.set(self.addr, r)
    self.dmx.set(self.addr + 1, g)
    self.dmx.set(self.addr + 2, b)
    self.dmx.set(self.addr + 3, int(159 + flashSpeedPercent * 96 / 100))

# American DJ LED Vision Moonflower
# 4 RGB sections, uses 12 DMX channels
class ADJ_LED_Vision:
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def clear(self):
    for i in range(0, 4): self.set(i, 0, 0, 0)

  def set(self, section, r, g, b):
    assert section >= 0 and section <= 3
    a = self.addr + section * 3
    self.dmx.set(a, r)
    self.dmx.set(a + 1, g)
    self.dmx.set(a + 2, b)

  def setAll(self, r, g, b):
    for i in range(0, 4): self.set(i, r, g, b)

# Eurolite LED PT-100 DMX Pixel Tube
# 16 RGB sections, uses 48 DMX channels
class Eurolite_LED_PT100:
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def clear(self):
    for i in range(0, 16): self.set(i, 0, 0, 0)

  def set(self, section, r, g, b):
    assert section >= 0 and section <= 15
    a = self.addr + section * 3
    self.dmx.set(a, r)
    self.dmx.set(a + 1, g)
    self.dmx.set(a + 2, b)

  def setAll(self, r, g, b):
    for i in range(0, 16): self.set(i, r, g, b)

# Fun Generation LED Diamond Dome MK II
# uses 9 DMX channels
class FunGeneration_LED_Diamond_Dome_MK_II:
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def clear(self):
    self.set()

  def set(self, r = 0, g = 0, b = 0, white = 0, amber = 0, uv = 0, strobe = 0, motor = 0, effect = 0):
    # set color channels:
    self.dmx.set(self.addr, r)
    self.dmx.set(self.addr + 1, g)
    self.dmx.set(self.addr + 2, b)
    self.dmx.set(self.addr + 3, white)
    self.dmx.set(self.addr + 4, amber)
    self.dmx.set(self.addr + 5, uv)

    # 0-9: Off; 10-255: strobe on, speed increasing
    self.dmx.set(self.addr + 6, strobe)

    # 0-5: motor off, static position; 6-127: motor position; 128-255: motor speed
    self.dmx.set(self.addr + 7, motor)

    #   0- 50: random effect
    #  51-100: 2 colors switching, motor speed increasing
    # 101-150: all colors switching, motor speed increasing
    # 151-200: all colors crossfading, motor speed increasing
    # 201-250: sound mode 1
    # 251-255: sound mode 2
    self.dmx.set(self.addr + 8, effect)
