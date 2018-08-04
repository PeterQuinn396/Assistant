'''
For running this file you need 'playsound' library (pip install playsound)

You also need to set up your Google credentials and install the library, see:
    https://cloud.google.com/text-to-speech/docs/reference/libraries
You might have to restart your computer for the environment variable changes to take affect
Don't lose your .json credential file!

The different voices that can be used can be found at:
    https://cloud.google.com/text-to-speech/docs/voices
The wavenet type voices sound far superior to the standard voices

'''
from playsound import playsound
from google.cloud import texttospeech
import os
import sys


class WavenetVoice:

    def __init__(self, voice_name='en-US-wavenet-c', language_code='en-US'):
        self.voice_name = voice_name
        self.language_code = language_code

    # [START tts_synthesize_text]
    def _synthesize_text(self, text, filename='output.mp3'):
        """Synthesizes speech from the input string of text."""
        '''filename should end with .mp3'''

        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.types.SynthesisInput(text=text)

        # Google API notes
        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.types.VoiceSelectionParams(language_code=self.language_code, name=self.voice_name)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(input_text, voice, audio_config)

        # The response's audio_content is binary.
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

    # [END tts_synthesize_text]

    def say(self, text):  # method to quickly generate, play and delete a sound file

        self._synthesize_text(text)
        playsound("output.mp3")
        try:
            #os.remove("output.mp3")
            pass
        except OSError:
            pass

    def create_sound_file(self, text, filename):  # can be used to create and store a sound file for later
        self._synthesize_text(text, filename)     # reduces calls to the Google server, maybe making it faster
                                                  # can also be used to reduce the burden on your free trial

    def play_sound_file(self, filename):  # plays a sound file
        playsound(filename)

    def create_wave(self, text): 
        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.types.SynthesisInput(text=text)

        # Google API notes
        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.types.VoiceSelectionParams(language_code=self.language_code, name=self.voice_name)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(input_text, voice, audio_config)
        
        with open('wavefile.wav', 'wb') as out:
            out.write(response.audio_content)
              

if __name__ == '__main__': # This code can say a string passed to it on the command line when run

    print("Starting")
    if len(sys.argv) == 2:
        words = str(sys.argv[1])
        voice = WavenetVoice()
        voice.say(words)
    else:
        print("Incorrect number of arguments")
        print("Provide only argument: the text to say")

