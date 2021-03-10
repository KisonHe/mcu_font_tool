#include "Kstrings.h"


namespace Kstrings{
Languages currentLanguage;
//>>KstringsCPP Start
const char* EnglishStrings[] = {"English", "Hello", "This is an English String", "This is an English String"};
const char* ChineseStrings[] = {"简体中文", "你好", "Except Chinese!", "This is an English String"};
const char* JapaneseStrings[] = {"日本語", "こんにちは", "This is an English String", "This is an English String"};
const char** namelist[] = {EnglishStrings ,ChineseStrings ,JapaneseStrings};
//>>KstringsCPP End
    int setLanguage(Languages Language){
        currentLanguage = Language;
        return 0;   // TODO
    }
    const char* getStringByName(Names name){
        return namelist[currentLanguage][name];
    }
}


// balabala