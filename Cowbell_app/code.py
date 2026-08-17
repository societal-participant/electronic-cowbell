# SPDX-License-Identifier: MIT
"""
Motion-Activated Cowbell
Adafruit RP2040 Prop-Maker Feather

Uses the board's built-in LIS3DH accelerometer to detect movement and
its built-in I2S amp to play a WAV file through the speaker.

Behavior:
- No movement -> silence
- Movement detected -> play immediately (no delay)
- If another movement is detected while the WAV is still playing, it
  restarts from the beginning -- so the faster/more often you shake it,
  the faster it re-clanks, tracking your shake rate directly.

NOTE ON VOLUME: this version streams the WAV straight from the
filesystem (like the original), rather than loading/boosting it fully
into RAM. That in-RAM approach hit the RP2040's ~264KB total SRAM
ceiling on a longer WAV file -- there just isn't room to hold a large
sample resident in memory permanently on this chip. If you want the
sound louder, boost the WAV file ITSELF once in Audacity
(Effect > Amplify or Normalize), then re-export and copy it back onto
CIRCUITPY as cowbell.wav -- that costs nothing in RAM here, since the
gain is already baked into the file before it ever reaches the board.
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
MOVEMENT_THRESHOLD = 1.5     # m/s^2 of combined change to count as "movement"
                              # WHILE SILENT -- keep this as your normal
                              # sensitivity for a genuine idle-to-shake trigger.
MOVEMENT_THRESHOLD_WHILE_PLAYING = 6.0  # stricter threshold used ONLY while
                              # the wav is already playing. The speaker's own
                              # vibration through the plastic shell can look
                              # like "motion" to the accelerometer and
                              # retrigger itself in a loop -- a real shake
                              # is a much bigger acceleration spike than
                              # that self-induced rattle, so raising the bar
                              # here specifically (not all the time) filters
                              # out the feedback while still letting a
                              # genuinely hard/fast shake override and
                              # retrigger. If it's still looping, raise this
                              # further (try 6-8); if genuine rapid shakes
                              # stop retriggering, lower it back down.
RETRIGGER_COOLDOWN = 0.15    # small debounce ONLY -- just enough to keep a
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

    # Use the stricter threshold while sound is actively playing, so the
    # speaker's own vibration doesn't retrigger itself in a feedback loop.
    active_threshold = (
        MOVEMENT_THRESHOLD_WHILE_PLAYING if mixer.voice[0].playing else MOVEMENT_THRESHOLD
    )

    now = time.monotonic()
    if delta > active_threshold and (now - last_trigger_time) > RETRIGGER_COOLDOWN:
        last_trigger_time = now
        play_wav()  # plays immediately, restarting from the beginning even
                     # if already playing -- no artificial delay in the way

    time.sleep(0.02)  # tighter poll loop than before, so quick shakes aren't
                        # missed between sensor reads
