class OctoPod75: # Conrad OctoPod OP-75 RGB-LED-Spot
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def set(self, r, g, b, flashSpeedPercent = 0):
    assert flashSpeedPercent >= 0 and flashSpeedPercent <= 100
    self.dmx.set(self.addr, r)
    self.dmx.set(self.addr + 1, g)
    self.dmx.set(self.addr + 2, b)
    self.dmx.set(self.addr + 3, 159 + flashSpeedPercent * 96 / 100)

class ADJ_LED_Vision: # American DJ LED Vision Moonflower
  def __init__(self, dmx, addr):
    self.dmx = dmx
    self.addr = addr

  def set(self, section, r, g, b):
    assert section >= 0 and section <= 3
    a = self.addr + section * 3
    self.dmx.set(a, r)
    self.dmx.set(a + 1, g)
    self.dmx.set(a + 2, b)
