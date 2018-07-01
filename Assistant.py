import os

import sys #for getting to the AIY folder
sys.path.insert(0, '/AIY-projects-python')

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('blink')
    recognizer.expect_phrase('computer')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'goodbye' in text:
                break


if __name__ == '__main__':
    main()