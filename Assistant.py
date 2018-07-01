import os

import aiy.audio
import aiy.cloudspeed
import aiy.voicehat

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn on light')
    recognizer.expect_phrase('turn off light')
    recognizer.expect_phrase('blink')
    recognizer.expect_phrase('computer')

    button = aiy.voicehat.get_button()
    led = aiy.