#!/usr/bin/python3
import sys
import _thread
import signal
import time
import random
import dmxudp
import enttec_esp
import fixtures

def exithandler(signal, frame):
  dmx.reset()
  print("\nExit!")
  sys.exit(0)

def OctoFlash():
  delay = .1 #.1
  #a = 7
  while True:
    #op[a].set(255, 0, 0)
    #op[a].set(255, 0, 0, 50)
    #time.sleep(delay)
    #op[a].set(0, 255, 0)
    #time.sleep(delay)
    #op[a].set(0, 0, 255)
    op[random.randint(0, 7)].set(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    time.sleep(delay)

def Moonflower():
  delay = .2
  while True:
    mflower.set(random.randint(0, 3), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    time.sleep(delay)

def PixelTubes():
  delay = .2
  while True:
    i = random.randint(0, 15)
    pixtube[0].clear()
    pixtube[0].set(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #pixtube[0].setAll(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pixtube[1].clear()
    pixtube[1].set(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    time.sleep(delay)

def setAllLamps(r, g, b):
  for i in range(0, 8): op[i].set(r, g, b)
  for i in range(0, 2): pixtube[i].setAll(r, g, b)
  for i in range(0, 4): mflower.set(i, r, g, b)

def GlobalEffects():
  delay = .2
  while True:
    effect = random.randint(0, 2)
    if effect == 0: # all red
      setAllLamps(255, 0, 0)
    elif effect == 1: # all green
      setAllLamps(0, 255, 0)
    elif effect == 2: # all blue
      setAllLamps(0, 0, 255)
    time.sleep(delay)

#dmx = dmxudp.DMXUDP("192.168.4.193", 8000)
dmx = enttec_esp.ENTTEC_ESP("192.168.4.179")

signal.signal(signal.SIGINT, exithandler)

op = []
for i in range(1, 8 * 4, 4): op.append(fixtures.OctoPod75(dmx, i))

#ms = [fixtures.Showtek_Microspot(dmx, 33), fixtures.Showtek_Microspot(dmx, 46)]
#es = fixtures.ADJ_EmeraldScanII(dmx, 59)
mflower = fixtures.ADJ_LED_Vision(dmx, 64)
pixtube = [fixtures.Eurolite_LED_PT100(dmx, 76), fixtures.Eurolite_LED_PT100(dmx, 124)]
# Next free address: 172

try:
  #_thread.start_new_thread(OctoFlash, ())
  #_thread.start_new_thread(Moonflower, ())
  #_thread.start_new_thread(PixelTubes, ())
  _thread.start_new_thread(GlobalEffects, ())
except:
  print("Error starting thread!")

while True:
  dmx.flush()
  time.sleep(1.0 / 40)
