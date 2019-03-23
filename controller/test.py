#!/usr/bin/python
import sys
import thread
import signal
import time
import random
import dmxudp
import fixtures

def exithandler(signal, frame):
  dmx.reset()
  sys.exit(0)

def OctoFlash():
  delay = 5 #.1
  while True:
    #op[7].set(255, 0, 0)
    op[7].set(255, 0, 0, 50)
    time.sleep(delay)
    op[7].set(0, 255, 0)
    time.sleep(delay)
    op[7].set(0, 0, 255)
    time.sleep(delay)

def Moonflower():
  delay = .2
  while True:
    mflower.set(random.randint(0, 3), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    time.sleep(delay)

dmx = dmxudp.DMXUDP("192.168.4.193", 8000)
#dmx = dmxudp.DMXUDP("127.0.0.1", 8000)

signal.signal(signal.SIGINT, exithandler) # http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python

op = []
for i in range(1, 8 * 4, 4):
  op.append(fixtures.OctoPod75(dmx, i))

mflower = fixtures.ADJ_LED_Vision(dmx, 64)

try:
  thread.start_new_thread(OctoFlash, ()) # https://www.tutorialspoint.com/python/python_multithreading.htm
  thread.start_new_thread(Moonflower, ())
except:
  print "Error starting thread!"

while True:
  dmx.flush()
  time.sleep(.2)
