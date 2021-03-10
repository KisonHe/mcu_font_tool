#ifndef STRINGS_H
#define STRINGS_H

// #include <string>
// using std::string;

#include <Arduino.h>

namespace Kstrings{
//>>KstringsH Start
enum Names{Hello, EnglishString, EnglishStringButChinese, LanguageName};
enum Languages{English, Chinese, Japanese};
//>>KstringsH End
    int setLanguage(Languages Language);
    const char* getStringByName(Names name);
}

#endif