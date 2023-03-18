# Kison's mcu font tool
Inspired by lvgl's lv_i18n & t123yh's mcufont-encoder

## Note
It don't work gettext style. You declare before use of text.

## How to use
1. Read the `strings.yaml` in [example](./example) to see how to define texts
2. Define your text FIRST and translations as `example.yaml` shows.
3. Run this tool before compile to generate right headers and functions.
4. Optional, Run this tool to generate list of out put to your font converter like `lv_font_conv`. Now only `lv_font_conv` is supported.
5. Optional , Run this tool to call the convert and do upload hook stuff etc...

Go to [example](./example) folder for more info

There is also a demo use in https://github.com/KisonHe/at32-gcc-template/, on branch mcu-font-tool-demo

## Missing Icons

If you use https://fonts.google.com/icons like me, you will notice that the ttf downloaded from google (MaterialIcons-Regular.ttf) is missing sooooooo many chars. 

You can build your own font from svg, and pass the font to this tool. 

```python
import fontforge
font = fontforge.font()
glyph = font.createChar(65, "font1")
glyph.importOutlines("xxx.svg")
font.generate("output.ttf")
```

## Why not lvgl's i18n tool
- It helps you with the font managing.

## Rules
1. If the translation is not available on the selected locale then the default language will be used instead
2. If the translation is not available on the default locale, the text ID will be returned

## What will this do for you 
1. Read info from config and string yaml files
2. Generate `stringtable.cpp/h` from [jinja](https://jinja.palletsprojects.com) template
   1. Get your text from ID
   2. Get text font from ID
3. Generate converter commands from template (Optional)
4. Run commands generated
5. Run defined upload command


## What this tool will not do for you 
1. Change the fonts. Take lvgl for example, if some text have different font for same ID, Language in [example.yaml](./example/example.yaml) for example, the text is not updated. If you update the font without updating its font, you will have a bad day. I recommend reboot to apply.
2. Update the strings. You need to set all instances'(lvgl labels) strings your self
3. Handling plural stuff
4. Thread safety

## TODO:
1. Allow generate `stringtable.h` from [inja](https://github.com/pantor/inja) template.
