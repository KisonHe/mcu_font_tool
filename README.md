# Kison's mcu font tool
Inspired by lvgl's lv_i18n & t123yh's mcufont-encoder

## Note
It don't work gettext style. You declare before use of text.

## How to use
1. Define your text FIRST and translations as `example.yaml` shows.
2. Run this tool before compile to generate right headers and functions.
3. Optional, Run this tool to generate list of out put to your font converter like `lv_font_conv`. Now only `lv_font_conv` is supported.
4. Optional , Run this tool to call the convert and do upload hook stuff etc...

Go to [example](./example) folder for more info

## Why not lvgl's i18n tool
- It helps you with the font managing.

## Rules
1. If the translation is not available on the selected locale then the default language will be used instead
2. If the translation is not available on the default locale, the text ID will be returned

## What will this do for you 
1. Generate a file with needed chars to pass to font generate(lv_font_conv) for you 
2. Offer function to get text from name
3. Offer function to get font from name(For now only `lv_font_t * `)
4. Generate function to load font from 
5. (Someday)With post upload feature(in pio), auto upload the (spiffs) file to target(esp32)


## What this tool will not do for you 
1. Change the fonts. Take lvgl for example, if some text have different font for same ID, Language in [example.yaml](./example/example.yaml) for example, the text is not updated. If you update the font without updating its font, you will have a bad day. I recommend reboot to apply.
2. Update the strings. You need to set all instances'(lvgl labels) strings your self
3. Handling plural stuff
4. Thread safety

## TODO:
1. Allow generate `stringtable.h` from [inja](https://github.com/pantor/inja) template.
