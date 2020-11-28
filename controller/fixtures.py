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
