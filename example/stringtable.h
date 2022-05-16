/**
 * Generated File, Do not modify
 * 
 */
#ifndef KH_STRING_TABLE_STRINGS_H
#define KH_STRING_TABLE_STRINGS_H
#include "user_conf.h"
#include <stdint.h>

namespace strings
{
    typedef struct {
        const char * text;
        const fonttype * font;
    } kh_textdata_t;
    typedef enum : uint8_t{
        English, Chinese, EndOfLanguages
    }Language_t;

    typedef enum : uint16_t {
        Language,TemperatureIcon,BrightnessIcon,FirmwareVersion,CurveInfoPower,BrightnessPercentage,LanguageName,EndOfTexts
    }ID;

    enum FontID : uint8_t {
        ui,ui_25,mono_25,mono_16,icon,icon_17,EndOfFonts
    };

    /**
     * @brief Get text from text ID
     * 
     * @param id ID of the text
     * @return const char* 
     */

    const char * kh_fonttool_get_text(ID id);
    /**
     * @brief Get font ptr from text ID
     * 
     * @param id ID of the text
     * @return const fonttype* 
     */
    const fonttype * kh_fonttool_get_font(ID id);

    /**
     * @brief Set the lang. The lib is volatile so saving data to storage yourself
     * 
     * @param lang The Language
     * @return int 0 normal, -1 if wrong index
     */
    int kh_fonttool_set_lang(Language_t lang);

}

#endif