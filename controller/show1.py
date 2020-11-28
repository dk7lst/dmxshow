#!/usr/bin/python3
import sys
import threading
import signal
import time
import random
import ENTTEC_ESP
import Fixtures
import BeatSync
import EffectLib

def exithandler(signal, frame):
  dmx.reset()
  print("\nExit!")
  sys.exit(0)

def setAllLamps(r, g, b):
  for i in range(0, len(op)): op[i].set(r, g, b)
  for i in range(0, len(pixtube)): pixtube[i].setAll(r, g, b)
  for i in range(0, 4): mflower.set(i, r, g, b)

def AllLampsRandom():
  (r, g, b) = EffectLib.getRandomColor()
  setAllLamps(r, g, b)

def Random1():
  step = random.randint(0, 6)
  (r, g, b) = EffectLib.getRandomColor()
  dmx.clear()
  if step == 0:
    op[1].set(r, g , b)
    op[6].set(r, g , b)
  elif step == 1:
    op[3].set(r, g , b)
    op[7].set(r, g , b)
  elif step == 2:
    op[1].set(r, g , b)
    op[2].set(r, g , b)
    op[3].set(r, g , b)
  elif step == 3:
    op[6].set(r, g , b)
    op[7].set(r, g , b)
  elif step == 4:
    op[4].set(r, g , b)
    op[5].set(r, g , b)
    op[6].set(r, g , b)
  elif step == 5:
    op[0].set(r, g , b)
    op[1].set(r, g , b)
  elif step == 6:
    op[0].set(r, g , b)
    op[1].set(r, g , b)
    for i in range(0, len(pixtube)): pixtube[i].setAll(r * .8, g * .8, b * .8)

def CenterWave():
  col = EffectLib.getRandomColor()
  op[5].set(col[0], col[1], col[2])
  CenterWave.history.insert(0, col)
  for i in range(0, min(len(CenterWave.history), 16)):
    (r, g, b) = CenterWave.history[i]
    brightness = (16 - i) / 16
    pixtube[0].set(i, r * brightness, g * brightness, b * brightness)
    pixtube[1].set(15 - i, r * brightness, g * brightness, b * brightness)
  while len(CenterWave.history) > 16: CenterWave.history.pop()
CenterWave.history = []

def DancingPixels(mirror, flashProbability):
  (r, g, b) = EffectLib.getRandomColor()
  if random.random() < flashProbability:
    pixtube[0].setAll(r, g, b)
    pixtube[1].setAll(r, g, b)
  else:
    i = random.randint(0, 15)
    pixtube[0].clear()
    pixtube[0].set(i, r, g, b)
    if mirror: i = 15 - i
    pixtube[1].clear()
    pixtube[1].set(i, r, g, b)

def VuMeters():
  for i in range(0, 2): VuMeters.vuValue[i] = VuMeters.vuMax[i] = max(VuMeters.vuValue[i], random.randint(7, 15))

def GlobalEffectsThread():
  global globalEffect
  while True:
    BeatSync.waitBeat()
    if random.randint(0, 100) < 5: globalEffect = random.randint(3, 8)
    if globalEffect == 0: # all red
      setAllLamps(255, 0, 0)
    elif globalEffect == 1: # all green
      setAllLamps(0, 255, 0)
    elif globalEffect == 2: # all blue
      setAllLamps(0, 0, 255)
    elif globalEffect == 3:
      AllLampsRandom()
    elif globalEffect == 4:
      Random1()
    elif globalEffect == 5:
      CenterWave()
    elif globalEffect == 6:
      DancingPixels(False, .1)
    elif globalEffect == 7:
      DancingPixels(True, .1)
    elif globalEffect == 8:
      VuMeters()

dmx = ENTTEC_ESP.ENTTEC_ESP("192.168.4.179")

signal.signal(signal.SIGINT, exithandler)

op = []
for i in range(1, 8 * 4, 4): op.append(Fixtures.OctoPod75(dmx, i))

#ms = [Fixtures.Showtek_Microspot(dmx, 33), Fixtures.Showtek_Microspot(dmx, 46)]
#es = Fixtures.ADJ_EmeraldScanII(dmx, 59)
mflower = Fixtures.ADJ_LED_Vision(dmx, 64)
pixtube = [Fixtures.Eurolite_LED_PT100(dmx, 76), Fixtures.Eurolite_LED_PT100(dmx, 124)]
# Next free address: 172

globalEffect = 8

threading.Thread(target=BeatSync.BeatSyncThread, daemon=True).start()
threading.Thread(target=GlobalEffectsThread, daemon=True).start()

VuMeters.vuValue = [0, 0]
VuMeters.vuMax = [0, 0]

while True:
  if globalEffect == 8:
    for i in range(0, 2):
      pixtube[i].clear()
      for x in range(0, int(VuMeters.vuValue[i])): pixtube[i].set(15 - x, x * 255 / 15, 100 - x * 100 / 15, 0)
      pixtube[i].set(15 - int(VuMeters.vuMax[i]), 255, 0, 0)
      if VuMeters.vuValue[i] > 0: VuMeters.vuValue[i] -= .5
  dmx.flush()
  time.sleep(1.0 / 40)
