import socket

# UDP-protocol for self-made Arduino interface
class DMXUDP:
  def __init__(self, ip, port):
    self.ip = ip
    self.udpport = port
    self.dmxbuf = bytearray(512)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.reset()

  def reset(self):
    self.clear()
    self.flush()

  def clear(self):
    for i in range(0, 512): self.dmxbuf[i] = 0

  def set(self, ch, val):
    val = int(val)
    assert ch >= 1 and ch <= 512
    assert val >= 0 and val <= 255
    self.dmxbuf[ch - 1] = val

  def flush(self):
    #print(''.join(format(x, '02X') for x in self.dmxbuf))
    self.sock.sendto(self.dmxbuf, (self.ip, self.udpport))
