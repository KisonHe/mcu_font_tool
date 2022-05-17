import fontprocessing
import endprocessing
import os
import os.path
import argparse
import yaml
import jinja2
from jinja2 import Template
from conf_lvgl_font_converter import conf_lvgl_font_converter_t
#TODO make path use config
#TODO the lvgl format
languages = []
ids = []
fonts = []
language_strs = []
font_ptrs = []
font_strs = []
default_lang = ""
font_text_dict = {} # {"ui":"alltexttogether",etc}
class font_complex_t:
    def __init__(self) -> None:
        self.TTF_Path = ""
        self.range_text = ""
        self.symbol_text = ""
        self.sub_pixel_text = ""
        self.size = 0
        self.bpp = 1
        self.format = ""
        self.filename = ""

font_complex_list = []

def font_name_to_font_str(fontname:str)->str:
    fontstr = "font_"+fontname.replace("-", "_").lower()# is spiffs case sensitive?
    return fontstr

def font_str_to_font_ptr(fontstr:str)->str:
    fontptr = fontstr+"_ptr"
    return fontptr


if __name__ == "__main__":
    # TODO: phase args
    parser = argparse.ArgumentParser(description="Kison's mcu font tool")
    parser.add_argument("-c","--config",help="Directory of config and strings yaml, default ./config",required=False, default="./config") 
    parser.add_argument("-t","--template",help="Directory of templates, default ./template",required=False, default="./template") 
    parser.add_argument("-o", "--output", help="Directory to Generate header and cpp file, default ../../src/gui",required=False) 
    # we assume user put this repo like this 
    # .
    # ├── include
    # ├── lib
    # ├── src
    # │   └── gui
    # ├── test
    # └── tools
    #     └── mcu_font_tool 
    parser.add_argument("-b", "--bash-output", help="Directory to Generate converter bash file, default ./scripts",required=False, default="./scripts")
    parser.add_argument("-r", "--run-bash", help="If run the generated converter bash file, default false",required=False, default=False)
    
    args = parser.parse_args()
    # phase args end
    lvgl_font_converter_conf = conf_lvgl_font_converter_t()
    try:
        pass # TODO: load config.yaml here
    except:
        pass
    
    try:    # load the string yaml
        yaml_path = os.path.join(args.config, "strings.yaml")
        stream = open(yaml_path, 'r')
        string_yaml_dict = yaml.safe_load(stream)
        stream.close()

        # generate languages
        if (not "Languages" in string_yaml_dict) or (len(string_yaml_dict["Languages"])<=1):
            raise ValueError
            pass
        default_lang = string_yaml_dict["Languages"][0].replace("-", "_")
        for l in string_yaml_dict["Languages"]:
            l.replace("-", "_")
            languages.append(l)
        # generate ids & fonts & font_text_dict
        for i in string_yaml_dict["Strings"]:
            text = i["ID"].replace("-", "_")
            ids.append(text)
            pass
        for i in string_yaml_dict["Fonts"]:
            text = i["Name"].replace("-", "_")
            fonts.append(text)
            text = font_name_to_font_str(text)
            font_strs.append(text)
            text = font_str_to_font_ptr(text)
            font_ptrs.append(text)
            font_text_dict[i["Name"]] = ""  #init the font_text_dict
            pass
        pass # TODO: load config.yaml here
    except:
        pass

    # open h template and save generated header
    try:
        hstring_template_file = open(os.path.join(args.template,"h_stringtable_template.inja"),"r")
        hstring_template_string = hstring_template_file.read()
        hstring_template_file.close()

        template = Template(hstring_template_string)
        header_render_result = template.render(languages=languages,ids=ids,fonts=fonts)
        h_file = open(os.path.join(args.output,"stringtable.h"),"w+")
        h_file.write(header_render_result)
        h_file.close()
        # print(header_render_result) #TODO save to file
        pass
    except:
        pass
    
    try: #generate language_strs
        for lang in string_yaml_dict["Languages"]: # outer loop
            strlist = []
            for text in string_yaml_dict["Strings"]:
                liststr = "{\""
                if ("Content-"+lang) in text:
                    font_text_dict[text["Content-"+lang]["Font"]] = font_text_dict[text["Content-"+lang]["Font"]] + text["Content-"+lang]["Value"]
                    liststr=liststr+text["Content-"+lang]["Value"]+"\", "
                    liststr=liststr+font_str_to_font_ptr(font_name_to_font_str(text["Content-"+lang]["Font"]))
                    liststr=liststr+"}"
                elif ("Content-all") in text:
                    font_text_dict[text["Content-all"]["Font"]] = font_text_dict[text["Content-all"]["Font"]] + text["Content-all"]["Value"]
                    liststr=liststr+text["Content-all"]["Value"]+"\", "
                    liststr=liststr+font_str_to_font_ptr(font_name_to_font_str(text["Content-all"]["Font"]))
                    liststr=liststr+"}"
                    pass
                else:
                    liststr=liststr+text["ID"]
                    liststr=liststr+"nullptr"
                    liststr=liststr+"}"
                    pass
                strlist.append(liststr)
                pass
            language_strs.append(strlist)
        pass
    except:
        pass

    # open c template and save generated header
    try:
        cstring_template_file = open(os.path.join(args.template,"c_stringtable_template.inja"),"r")
        cstring_template_string = cstring_template_file.read()
        cstring_template_file.close()

        template = Template(cstring_template_string)
        c_render_result = template.render(font_ptrs=font_ptrs,default_lang=default_lang,language_strs=language_strs,font_strs=font_strs)
        c_file = open(os.path.join(args.output,"stringtable.cpp"),"w+")
        c_file.write(c_render_result)
        c_file.close()
        pass
    except:
        pass

    # generate convert bash
    try:
        for i in string_yaml_dict["Fonts"]:
            tmp_font_complex = font_complex_t()
            tmp_font_complex.TTF_Path = i["TTF"]
            if ("SymbolUnicode" in i):
                tmp_font_complex.range_text="-r " + i["SymbolUnicode"] + ""
                pass
            else:
                tmp_font_complex.range_text=""
                pass
            tmp_font_complex.symbol_text = font_text_dict[i["Name"]] # no need to remove duplicate chars cause lvgl will handle that
            if lvgl_font_converter_conf.subpx == "H":
                tmp_font_complex.sub_pixel_text = "--lcd"
            elif lvgl_font_converter_conf.subpx == "V":
                tmp_font_complex.sub_pixel_text = "--lcd-v"
            else:
                tmp_font_complex.sub_pixel_text = ""
                pass
            tmp_font_complex.size = i["Size"]
            if ("bpp" in i):
                tmp_font_complex.bpp = i["bpp"]
                pass
            else:
                tmp_font_complex.bpp = "1"
                pass
            if (lvgl_font_converter_conf.output == "lvgl"):
                tmp_font_complex.format = "lvgl" 
                #todo the file name 
            else:
                tmp_font_complex.format = "bin" 
                tmp_font_complex.filename = font_name_to_font_str(i["Name"])+".bin"
            font_complex_list.append(tmp_font_complex)
        pass
    except:
        pass
    
    # open bash template and save generated commands
    try:
        bash_template_file = open(os.path.join(args.template,"converter_template.inja"),"r")
        bash_template_string = bash_template_file.read()
        bash_template_file.close()
        template = Template(bash_template_string)
        bash_render_result = template.render(ConverterCommand=lvgl_font_converter_conf.converter_command,font_complexs=font_complex_list)
        bash_file = open(os.path.join(args.bash_output,"converter.bash"),"w+")
        bash_file.write(bash_render_result)
        bash_file.close()
        pass
    except:
        pass
    pass



