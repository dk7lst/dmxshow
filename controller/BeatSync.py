import threading
import time

def waitBeat():
  with sync: sync.wait()

# Thread for beat clock based on sound beats. Time-driven for now.
def BeatSyncThread():
  while True:
    time.sleep(.2) # TODO: Get beats from audio signal
    with sync: sync.notify_all()

sync = threading.Condition()
