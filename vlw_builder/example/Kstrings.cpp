#include "Kstrings.h"

namespace Kstrings{
Languages currentLanguage;
uint8_t currentFont = 0xFF;
//>>KstringsCPP Start
const char* EnglishStrings[] = {"", "English"};
uint8_t Englishmap[] = {2, 0};
const char* ChineseStrings[] = {"", "简体中文"};
uint8_t Chinesemap[] = {2, 0};
const char* JapaneseStrings[] = {"", "日本語"};
uint8_t Japanesemap[] = {2, 1};
uint8_t* map[] = {Japanesemap, Japanesemap, Japanesemap};
const char** namelist[] = {EnglishStrings ,ChineseStrings ,JapaneseStrings};
const char* Fonts[] = {"toSerifCJKSCSemiBold25", "toSerifCJKSCSemiBold55", "MaterialIcons25"};
//>>KstringsCPP End
    int setLanguage(Languages Language){
        currentLanguage = Language;
        return 0;   // TODO
    }
    const char* getStringByName(Names name){
        return namelist[currentLanguage][name];
    }
    const char* getFontByName(Names name){
        return Fonts[map[currentLanguage][(uint8_t)(name)]];
    }
    int setFontByName(TFT_eSPI &tft, Names name, int force){
        if ((force) || (currentFont != map[currentLanguage][(uint8_t)(name)])){
            currentFont = map[currentLanguage][(uint8_t)(name)];
            tft.loadFont(getFontByName(name),true);
        }
        else {
            return 1;
        }
        return 0;
    }
}


// balabala