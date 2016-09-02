#!/usr/bin/python2.7

# Copyright (C) 2016 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import os
import time
import atexit
import ftdi1 as ftdi

# disconnecting the data pins doesn't seem to help reliability
DSHDN = 1
PEN = 2
SWITCH = 4

current = 0
c = None


def switch(mode):
  global c
  c = ftdi.new()
  # TODO(benjaminfair): error checking
  ftdi.usb_open_desc(c, 0x0403, 0x6001, None, os.environ.get("FTDI_SERIAL"))
  ftdi.set_bitmode(c, 0xFF, ftdi.BITMODE_BITBANG)
  atexit.register(ftdi.free, c)

  disable()

  if mode == 'run':
    set(SWITCH)
  elif mode == 'debug':
    clear(SWITCH)
  elif mode == 'disable':
    return

  enable()


def disable():
  #  set(DSHDN)
  clear(PEN)
  update()


def enable():
  update()
  time.sleep(1)
  set(PEN)
  update()


def update():
  #  print 'current is ' + bin(current)
  ftdi.write_data(c, str(chr(current)), 1)


def clear(mask):
  global current
  current &= ~mask


def set(mask):
  global current
  current |= mask


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Control the USB switcher.')
  parser.add_argument(
      'mode',
      choices=['run', 'debug', 'disable', 'enable'],
      nargs='?',
      help='what mode the USB switcher should be placed into')
  args = parser.parse_args()
  switch(args.mode)
