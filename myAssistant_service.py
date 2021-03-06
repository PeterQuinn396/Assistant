#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys
import threading
from WebhookServer import start_server

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
from time import sleep

# better voice than the default one
from WavenetVoice import WavenetVoice



""" Needs to be modified to use the google assisant service, as the google assisant library is now deprecated"""
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


# custom local commands
def power_off_pi():
    voice = WavenetVoice()
    voice.create_wave('Good Bye')
    aiy.audio.play_wave('wavefile.wav')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    voice = WavenetVoice()
    voice.create_wave('See you in a bit!')
    aiy.audio.play_wave('wavefile.wav')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    voice = WavenetVoice()
    voice.create_wave('My IP address is %s' % ip_address.decode('utf-8'))
    aiy.audio.play_wave('wavefile.wav')


def light_on():
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.ON)
    sleep(5)


def light_off():
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.OFF)
    sleep(5)


def blink():
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.BLINK)
    sleep(5)


def end_program():
    voice = WavenetVoice()
    voice.create_wave('ending program')
    aiy.audio.play_wave('wavefile.wav')
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.OFF)
    exit(0)


# this is the LUT for the phrases and local commands associated with them
local_cmds_dict = {
    'power off': power_off_pi,
    'reboot': reboot_pi,
    'ip address': say_ip,
    'light on': light_on,
    'light off': light_off,
    'blink': blink,
    'end program': end_program,
}


# this function is what actually runs our assistant
def process_event(assistant, event, dark_mode):
    status_ui = aiy.voicehat.get_status_ui()


    if event.type == EventType.ON_START_FINISHED:

        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()

        local_cmd = local_cmds_dict.get(text, 0)

        if text == 'run dark' or text == 'dark mode':
            assistant.stop_conversation()
            dark_mode = True
            return dark_mode
        elif text == 'lights on':
            assistant.stop_conversation()
            dark_mode = False
            return dark_mode
        elif local_cmd != 0:
            assistant.stop_conversation()
            local_cmd()


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        if dark_mode:
            status_ui.status('power-off')
        else:
            status_ui.status('ready')
        return dark_mode

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    dark_mode = False
    subprocess.call('export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Desktop/Assistant-fe54628ef7ab.json"', shell=True)
    with Assistant(credentials) as assistant:
       for event in assistant.start():
            dark_mode = process_event(assistant, event, dark_mode)


if __name__ == '__main__':

    # server_thread = threading.Thread(target=start_server, args=(1,), daemon=True)
    # server_thread.start()
    main()
