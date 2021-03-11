#include "Kstrings.h"


namespace Kstrings{
Languages currentLanguage;
uint8_t currentFont = 0xFF;
//>>KstringsCPP Start
const char* EnglishStrings[] = {"Hello", "This is an English String", "This is an English String", "English"};
const char* ChineseStrings[] = {"你好", "This is an English String", "Except Chinese!", "简体中文"};
const char* JapaneseStrings[] = {"こんにちは", "This is an English String", "This is an English String", "日本語"};
const char** namelist[] = {EnglishStrings ,ChineseStrings ,JapaneseStrings};
const char* Fonts[] = {"Maintext"};
uint8_t Englishmap[] = {0, 0, 0, 0};
uint8_t Chinesemap[] = {0, 0, 0, 0};
uint8_t Japanesemap[] = {0, 0, 0, 0};
uint8_t* map[] = {Englishmap, Chinesemap, Japanesemap};
//>>KstringsCPP End
    int setLanguage(Languages Language){
        currentLanguage = Language;
        return 0;   // TODO
    }
    const char* getStringByName(Names name){
        return namelist[currentLanguage][name];
    }
    const char* getFontByName(Names name){
        return Fonts[map[(uint8_t)(name)]];
    }
    int setLanguageByName(TFT_eSPI &tft, Names name, int force){
        if (currentFont == map[(uint8_t)(name)]){
            return 1;
        }
        else
            tft.loadFont(getFontByName(name),true);
        return 0;
    }
}


// balabala