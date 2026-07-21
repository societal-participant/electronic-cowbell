# SPDX-FileCopyrightText: 2026 Maggie Giles, mgilesxo@gmail.com
#
# SPDX-License-Identifier: MIT
"""
Motion-Activated Cowbell
Adafruit RP2040 Prop-Maker Feather

Uses the board's built-in LIS3DH accelerometer to detect movement and
its built-in I2S amp to play a WAV file through the speaker.

The adafruit_lis3dh.mpy library is required.

Behavior:
- No movement -> silence
- Movement detected -> play immediately (no delay)
- If another movement is detected while the WAV is still playing, it
  restarts from the beginning -- so the faster/more often you shake it,
  the faster it jingles, tracking your shake rate directly.

NOTE ON VOLUME: this version streams the WAV straight from the
filesystem rather than loading/boosting it fully into RAM.
If you want the sound louder, boost the WAV file itself.
"""

import time
import board
import audiocore
import audiobusio
import audiomixer
from digitalio import DigitalInOut, Direction
import adafruit_lis3dh

# ----------------- Settings you may want to tune -----------------
WAV_FILE = "cowbell.wav"     # name of your wav file on CIRCUITPY
MOVEMENT_THRESHOLD = 3.5     # m/s^2 of combined change to count as "movement"
RETRIGGER_COOLDOWN = 0.2    # small debounce ONLY -- just enough to keep a
                              # single shake from double-counting due to
                              # sensor noise. Keep this small so replay rate
                              # can actually track how fast you're shaking.
SAMPLE_RATE = 22050          # must match your wav file's sample rate
CHANNEL_COUNT = 2            # 1 = mono, 2 = stereo -- must match your wav file
# -------------------------------------------------------------------

# Power up the onboard amp + accelerometer rail
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True
time.sleep(0.1)  # give the amp a moment to wake up

# Set up the onboard LIS3DH accelerometer
i2c = board.I2C()
int1 = DigitalInOut(board.ACCELEROMETER_INTERRUPT)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Set up I2S audio output through the onboard amp
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)
mixer = audiomixer.Mixer(
    voice_count=1,
    sample_rate=SAMPLE_RATE,
    channel_count=CHANNEL_COUNT,
    bits_per_sample=16,
    samples_signed=True,
)
audio.play(mixer)
mixer.voice[0].level = 1.0  # make sure we're not leaving free headroom on the table

_current_wave_file = None


def play_wav():
    """(Re)open and play the wav file from the beginning. Streams from
    the filesystem rather than loading it all into RAM -- works
    regardless of how long the file is."""
    global _current_wave_file
    if _current_wave_file:
        _current_wave_file.close()
    _current_wave_file = open(WAV_FILE, "rb")
    wave = audiocore.WaveFile(_current_wave_file)
    mixer.voice[0].play(wave)


# Baseline reading so we can detect *changes* in acceleration rather than
# absolute values (which always include ~9.8 m/s^2 of gravity on some axis)
last_accel = lis3dh.acceleration
last_trigger_time = -RETRIGGER_COOLDOWN  # allow an immediate first trigger

while True:
    x, y, z = lis3dh.acceleration
    delta = abs(x - last_accel[0]) + abs(y - last_accel[1]) + abs(z - last_accel[2])
    last_accel = (x, y, z)

    now = time.monotonic()
    if delta > MOVEMENT_THRESHOLD and (now - last_trigger_time) > RETRIGGER_COOLDOWN:
        last_trigger_time = now
        play_wav()  # plays immediately, restarting from the beginning even
                     # if already playing -- no artificial delay in the way

    time.sleep(0.02)  # tighter poll loop than before, so quick shakes aren't
                        # missed between sensor reads
