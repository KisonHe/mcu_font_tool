#ifndef STRINGS_H
#define STRINGS_H

// #include <string>
// using std::string;

#include <Arduino.h>

namespace Kstrings{
//>>KstringsH Start
enum Names{CalibrationString, CalibrationItem, SaveCalibrationConfirm, Smile, RadioButtonEmpty, RadioButtonFilled, LanguageName};
enum Languages{English, Chinese};
//>>KstringsH End
    int setLanguage(Languages Language);
    const char* getStringByName(Names name);
}

#endif