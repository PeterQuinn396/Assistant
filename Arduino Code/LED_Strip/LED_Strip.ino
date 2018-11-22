#include <bitswap.h>
#include <chipsets.h>
#include <color.h>
#include <colorpalettes.h>
#include <colorutils.h>
#include <controller.h>
#include <cpp_compat.h>
#include <dmx.h>
#include <FastLED.h>
#include <fastled_config.h>
#include <fastled_delay.h>
#include <fastled_progmem.h>
#include <fastpin.h>
#include <fastspi.h>
#include <fastspi_bitbang.h>
#include <fastspi_dma.h>
#include <fastspi_nop.h>
#include <fastspi_ref.h>
#include <fastspi_types.h>
#include <hsv2rgb.h>
#include <led_sysdefs.h>
#include <lib8tion.h>
#include <noise.h>
#include <pixelset.h>
#include <pixeltypes.h>
#include <platforms.h>
#include <power_mgt.h>

#define NUM_LEDS 60
#define LEDPIN 6
#define DELAY 20

CRGB leds[NUM_LEDS];
char mode = 'z'; //default, strip off
char incByte;
byte brightness = 127;

//animation memory
byte counter = 0; //counter used in animations
byte blinkCnt = 40; //number of cycles*DELAY for a full on/off cycle for blink
byte moveCnt = 2; //number of cycles*DELAY to move pixels along
bool fadeInc = true;
void setup() {

  FastLED.addLeds<NEOPIXEL, LEDPIN>(leds, NUM_LEDS);
  FastLED.setBrightness(brightness);

  //colour is off to start
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
  FastLED.delay(DELAY);

  Serial.begin(9600);

}

void loop() {

  //grab new commands if something was sent over serial
  if (Serial.available() > 0) {
    // read the incoming byte:

    incByte = Serial.read();

    if (isDigit(incByte)) { //digits adjust brightness, takes 1-10
      incByte = incByte - '0';
      if (incByte == 0)
        incByte += 10; //zero is mapped to 10
      brightness = map(incByte, 1, 10, 25, 255);
      FastLED.setBrightness(brightness);
      FastLED.show();
      FastLED.delay(DELAY);

    } else {

      switch (incByte) {

        case 'z': //off/black
          fill_solid(leds, NUM_LEDS, CRGB::Black);
          FastLED.show();
          FastLED.delay(DELAY);
          break;

        case 'x': //set mode to x for no animation
          mode = 'x';
          break;

        case 'c': //fill in an RGB specified colour
          fill_solid(leds, NUM_LEDS, CRGB(Serial.read(), Serial.read(), Serial.read()));
          break;

        case 'w': //white
          fill_solid(leds, NUM_LEDS, CRGB::White);
          FastLED.show();
          FastLED.delay(DELAY);
          break;

        case 'r': //red
          fill_solid(leds, NUM_LEDS, CRGB::Red);
          FastLED.show();
          FastLED.delay(DELAY);
          break;

        case 'q': //rainbow
          fill_rainbow(leds, NUM_LEDS, 0, 255 / NUM_LEDS);
          FastLED.show();
          FastLED.delay(DELAY);
          break;

        case 'd': //random colours

          break;

      //animation modes
        case 'l':
          FastLED.setBrightness(brightness);
          mode = 'l';
          counter = 0;
          break;

        case 'm':
          FastLED.setBrightness(brightness);
          mode = 'm';
          counter = 0;
          break;

        case 'f':
          FastLED.setBrightness(brightness);
          mode ='f';
          counter = 0;
          bool fadeInc = true;
          break;
        
      }
    }
  }

  //animations, need to run every loop
  switch (mode) {

    case 'l': //blink

      if (counter < blinkCnt / 2) {
        FastLED.setBrightness(brightness);
        FastLED.show();
        FastLED.delay(DELAY);
      } else {
        FastLED.setBrightness(0);
        FastLED.show();
        FastLED.delay(DELAY);
      }
      counter++;
      counter  = counter % blinkCnt;
      break;

    case 'm': //colour moves and wraps

      if (counter == 0) {
        CRGB last = leds[0]; //save the last leds colour
        CRGB temp;
        for (byte i = 1; i < NUM_LEDS; i++) {
          temp = leds[i];
          leds[i] = last;
          last = temp;
        }
        leds[0] = last; //place last led colour in first position
        FastLED.show();
      }

      FastLED.delay(DELAY);
      counter++;
      counter  = counter % moveCnt;
      break;

    case 'f': //colour fades in and out / pulses
      FastLED.setBrightness(counter);
      FastLED.show();
      FastLED.delay(DELAY);

      if (fadeInc){ //increase brightness if we are below max brightness
       counter++;
      } else{
        counter--;
      }

      if (counter <= 4){ //min brightness value
        fadeInc = true;
      }
      if (counter >= brightness){
        fadeInc=false;
      }
     
      break;

    case 's': //color moves like a sin wave
      break;
  }

}
