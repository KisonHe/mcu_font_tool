#!/bin/bash

node ./node_modules/lv_font_conv/lv_font_conv.js --font sarasa-gothic-sc-regular.ttf -r 0x4E2D,0x56FD --symbols "LanguageFirmware: %s固件版本" --lcd --size 34 --bpp 4 --format bin -o font_ui.bin
node ./node_modules/lv_font_conv/lv_font_conv.js --font sarasa-gothic-sc-regular.ttf --symbols "语言English简体中文" --lcd --size 25 --bpp 1 --format bin -o font_ui_25.bin
node ./node_modules/lv_font_conv/lv_font_conv.js --font sarasa-fixed-sc-regular.ttf --symbols "%d%%" --lcd --size 25 --bpp 1 --format bin -o font_mono_25.bin
node ./node_modules/lv_font_conv/lv_font_conv.js --font sarasa-fixed-sc-regular.ttf --symbols "%g%.1f-%.1fV %g%.1f-%.1fA" --lcd --size 17 --bpp 1 --format bin -o font_mono_16.bin
node ./node_modules/lv_font_conv/lv_font_conv.js --font MaterialIcons.ttf --symbols "" --lcd --size 40 --bpp 1 --format bin -o font_icon.bin
node ./node_modules/lv_font_conv/lv_font_conv.js --font sarasa-gothic-sc-regular.ttf -r 0x4E2D,0x56FD --symbols "" --lcd --size 17 --bpp 1 --format bin -o font_icon_17.bin