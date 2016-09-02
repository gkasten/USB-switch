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

import time
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H

def switch(mode):
#  FT232H.use_FT232H()

  ft232h = FT232H.FT232H()

  ft232h.setup(8, GPIO.IN)
  ft232h.setup(9, GPIO.OUT)
  ft232h.output(9, GPIO.HIGH)
  ft232h.setup(10, GPIO.OUT)
  ft232h.output(10, GPIO.LOW)

  if mode == "toggle":
    do_toggle(ft232h)
  else:
    do_clear(ft232h)
    if mode == "run":
      do_toggle(ft232h)
    
def do_toggle(ft232h):
  ft232h.output(9, GPIO.LOW)
  time.sleep(0.1)
  ft232h.output(9, GPIO.HIGH)

def do_clear(ft232h):
  ft232h.output(10, GPIO.HIGH)
  time.sleep(0.1)
  ft232h.output(10, GPIO.LOW)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Control the USB switcher.")
  parser.add_argument("mode", choices=["toggle", "run", "debug"],
                      default="toggle", nargs='?',
                      help="what mode the USB switcher should be placed into")
  args = parser.parse_args()
  switch(args.mode)
