/**
 * Generated File, Do not modify
 * 
 */
#include "stringtable.h"
#include <stdint.h>
const fonttype* font_ui_ptr;
const fonttype* font_ui_25_ptr;
const fonttype* font_mono_25_ptr;
const fonttype* font_mono_16_ptr;
const fonttype* font_icon_ptr;
const fonttype* font_icon_17_ptr;
namespace strings
{
    Language_t CurrentLanguage = English; //When generating, set default to first lang

    static kh_textdata_t MainData[EndOfLanguages][EndOfTexts] = {
        {
            {"Language",font_ui_ptr},
            {"\uE1FF",font_icon_ptr},
            {"\ue1ae",font_icon_ptr},
            {"Firmware: %s",font_ui_ptr},
            {"%g%.1f-%.1fV %g%.1f-%.1fA",font_mono_16_ptr},
            {"%d%%",font_mono_25_ptr},
            {"English",font_ui_25_ptr},
        },{
            {"语言",font_ui_25_ptr},
            {"\uE1FF",font_icon_ptr},
            {"\ue1ae",font_icon_ptr},
            {"固件版本: %s",font_ui_ptr},
            {"%g%.1f-%.1fV %g%.1f-%.1fA",font_mono_16_ptr},
            {"%d%%",font_mono_25_ptr},
            {"简体中文",font_ui_25_ptr},
        }
    };
    
    static const char* FontNames[] = {  //help to load font from file system
        "font_ui",
        "font_ui_25",
        "font_mono_25",
        "font_mono_16",
        "font_icon",
        "font_icon_17"
    };

    const char * kh_fonttool_get_text(ID id){
        if (id >= EndOfTexts)
            return nullptr;
        return MainData[CurrentLanguage][id].text;
    }

    const fonttype * kh_fonttool_get_font(ID id){
        if (id >= EndOfTexts)
            return nullptr;
        return MainData[CurrentLanguage][id].font;
    }

    int kh_fonttool_set_lang(Language_t lang){
        if (lang >= EndOfLanguages)
            return -1;
        CurrentLanguage = lang; 
        return 0; 
    }
  
}
