from conf_font_converter import conf_font_converter_t

class conf_lvgl_font_converter_t(conf_font_converter_t):
    output = "bin"
    converter_command = "lv_font_conv"
    subpx = "None"