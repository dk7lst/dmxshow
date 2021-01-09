#!/usr/bin/python3
import math
import numpy as np # https://numpy.org/doc/stable/
import wave # https://docs.python.org/3/library/wave.html
import matplotlib.pyplot as plt # https://matplotlib.org/tutorials/introductory/pyplot.html

# Define frequency ranges of interest:
#FreqBands = [(20, 100), (1000, 2000), (4000, 5000)]
FreqBands = [(20, 100)]

def processWaveFile(filename):
  wf = wave.open(filename,'rb')

  AudioChannels = wf.getnchannels()
  AudioSampleWidth = wf.getsampwidth()
  AudioSampleRate = wf.getframerate()
  AudioFramesInFile = wf.getnframes()

  print("AudioFile = \"" + filename + "\"")
  #print("getparams() = " + str(wf.getparams()))
  print("AudioChannels = " + str(AudioChannels))
  print("AudioSampleWidth = " + str(AudioSampleWidth) + " Bytes")
  print("AudioSampleRate = " + str(AudioSampleRate) + " Hz")
  print("AudioFramesInFile = " + str(AudioFramesInFile) + " Frames")
  print("AudioLength = " + str(round(AudioFramesInFile / AudioSampleRate, 1)) + " s")

  #CHUNKSEC = 0.1 # Process audio in chunks of 1/10 sec.
  CHUNKSEC = 1.0 / 60
  CHUNKFRAMES = int(AudioSampleRate * CHUNKSEC)

  BandHistory = []

  while True:
    AudioBytes = wf.readframes(CHUNKFRAMES) # byte-array
    if AudioBytes == b'': break
    BandPwr = frequencyAnalysis(AudioBytes, AudioSampleRate, AudioChannels, AudioSampleWidth)
    #print(BandPwr)
    BandHistory.append(BandPwr)

    #findBeats()
    #break # test

  plt.plot(BandHistory, '.-r')
  plt.show()

def frequencyAnalysis(AudioBytes, AudioSampleRate, AudioChannels, AudioSampleWidth):
  assert(len(AudioBytes) % (AudioChannels * AudioSampleWidth) == 0) # only complete frames allowed
  assert(AudioChannels == 1 or AudioChannels == 2) # mono or stereo input
  assert(AudioSampleWidth == 2) # Assume 16 bit signed little endian samples

  # Convert to 1d-array with channels interleaved, then convert to float:
  audio = np.frombuffer(AudioBytes, dtype=np.int16).astype(float)

  # Stereo-to-mono down-mix required?
  if AudioChannels == 2:
    # Re-shape array into 2d-array in order to separate channels. Then average stereo channels for mono signal:
    audio = audio.reshape(-1, AudioChannels).sum(axis=1) / 2

  # FFT:
  fourier = np.fft.fft(audio)
  freq = np.fft.fftfreq(audio.size, d=1.0/AudioSampleRate)

  # Split/sum frequencies into bands:
  BandPwr = np.zeros(len(FreqBands))
  for i in range(0, int(len(freq) / 2)): # Use only first half, skip negative frequencies as they just mirror the positives
    f = freq[i]
    a = abs(fourier.imag[i])
    #print(f, a)
    for bandIdx in range(0, len(FreqBands)):
      if f >= FreqBands[bandIdx][0] and f < FreqBands[bandIdx][1]:
        BandPwr[bandIdx] += a
        break

  # Normalize to band width and logarithmize:
  for bandIdx in range(0, len(FreqBands)):
    BandPwr[bandIdx] = math.log(1 + BandPwr[bandIdx] / (FreqBands[bandIdx][1] - FreqBands[bandIdx][0]), 10)

  #plt.plot(freq, fourier.imag)
  #plt.show()
  return BandPwr

# Process test file:
#processWaveFile('running.wav')
processWaveFile('tanzen.wav')
#processWaveFile('sin50hz.wav')
