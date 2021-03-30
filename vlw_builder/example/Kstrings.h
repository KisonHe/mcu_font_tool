#ifndef STRINGS_H
#define STRINGS_H

// #include <string>
// using std::string;
#include <stdint.h>
#include "TFT_eSPI.h"
// #include <Arduino.h>

namespace Kstrings{

//>>KstringsH Start
enum Names{FingerPrint, LanguageName};
enum Languages{English, Chinese, Japanese};
//>>KstringsH End
    int setLanguage(Languages Language);
    const char* getStringByName(Names name);
    const char* getFontByName(Names name);
    // use a var to store font loaded
    // tft_espi lib's tft.loadFont seems wont check 
    // current loaded font, so a force update is optional
    int setFontByName(TFT_eSPI &tft, Names name, int force = 0);
}

#endif