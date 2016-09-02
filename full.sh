#!/bin/bash

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

./switch2.py debug
echo "Waiting for device..."
adb wait-for-device

echo "Granting permission"
adb shell pm grant org.chromium.latency.walt android.permission.READ_EXTERNAL_STORAGE
adb shell pm grant org.chromium.latency.walt android.permission.WRITE_EXTERNAL_STORAGE

echo "Starting test"
adb shell am start -a org.chromium.latency.walt.START_TEST -n org.chromium.latency.walt/.MainActivity --ei Reps 100 --es TestType MidiIn --es FileName "/sdcard/data.csv"
./switch2.py run

echo "Waiting for results... (Press enter to continue early)"
read -t 10

./switch2.py debug
echo "Waiting for device..."
adb wait-for-device

echo "Fetching results"
adb pull /sdcard/data.csv $1
