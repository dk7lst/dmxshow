import time
import threading
import rtmidi # https://spotlightkid.github.io/python-rtmidi/

# Docs:
# - https://spotlightkid.github.io/python-rtmidi/
#   - https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn
# - https://en.wikipedia.org/wiki/MIDI_beat_clock

# Use MIDI Beat Clock for sound-to-light sync. Needs a mixing console with beat counter and midi output.
class MidiSync:
  def MidiRxHandler(msgtuple, data):
    msg, timediff = msgtuple
    if msg != [248]: return # we only care about clock messages
    data.clock = data.clock + 1
    if data.clock < 24: return # 24 MIDI clock ticks per beat (1/4 note)
    with data.sync: data.sync.notify_all()
    t = time.time()
    data.bpm = 60 / (t - data.lastBeatTime)
    if data.printBPM: print("BPM: %.1f" % (data.bpm))
    data.lastBeatTime = t
    data.clock = 0

  def __init__(self, printBPM = False):
    self.printBPM = printBPM
    self.midi_in = rtmidi.MidiIn()
    self.midi_in.ignore_types(sysex=True, timing=False, active_sense=True)
    self.sync = threading.Condition()
    self.clock = 0
    self.lastBeatTime = 0
    self.bpm = 0
    self.midi_in.set_callback(MidiSync.MidiRxHandler, data=self)

  def getAvailablePorts(self):
    return self.midi_in.get_ports()

  def openPort(self, portidx = 0):
    self.midi_in.open_port(portidx)
    return self.midi_in.is_port_open()

  def getBPM(self):
    return self.bpm

  def waitBeat(self):
    with self.sync: self.sync.wait()
