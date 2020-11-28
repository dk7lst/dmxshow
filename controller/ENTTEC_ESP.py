import socket

# ENTTEC ESP DMX-over-Ethernet-protocol 1.5
# https://www.enttec.co.uk/en/product/controls/dmx-ethernet-lighting-control/power-over-ethernet-dmx-interface/
# http://dol2kh495zr52.cloudfront.net/pdf/misc/ESP_Specs.pdf
# TODO: Implement node auto-discovery.
class ENTTEC_ESP:
  def __init__(self, ip, universe = 0):
    self.ip = ip
    self.udpport = 3333
    self.dmxbuf = bytearray(bytes('ESDD', 'utf-8')
      + universe.to_bytes(1, 'big')
      + (0).to_bytes(1, 'big') # DMX Start Code (default 0)
      + (1).to_bytes(1, 'big') # Data Type 1 (up-to 512 bytes of DMX DATA)
      + (512).to_bytes(2, 'big') # Size of data block
      ) + bytearray(512) # DMX channel bytes
    self.headersize = 9
    assert len(self.dmxbuf) == self.headersize + 512
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.reset()

  def reset(self):
    self.clear()
    self.flush()

  def clear(self):
    for i in range(self.headersize, self.headersize + 512): self.dmxbuf[i] = 0

  def set(self, ch, val):
    val = int(val)
    assert ch >= 1 and ch <= 512
    assert val >= 0 and val <= 255
    self.dmxbuf[self.headersize + ch - 1] = val

  def flush(self):
    #print(''.join(format(x, '02X') for x in self.dmxbuf))
    self.sock.sendto(self.dmxbuf, (self.ip, self.udpport))
