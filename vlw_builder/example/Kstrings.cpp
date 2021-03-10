
#include "Kstrings.h"


namespace Kstrings{
Languages currentLanguage;
//>>KstringsCPP Start
const char* EnglishStrings[] = {"Save calibration?", "校准项目", "English", "Calibration", "", "", ""};
const char* ChineseStrings[] = {"校准", "校准项目", "保存吗", "简体中文", "", "", ""};
//>>KstringsCPP End
    int setLanguage(Languages Language){
        return 0;
    }
    const char* getStringByName(Names name){
        return EnglishStrings[0];
    }
}


// balabala