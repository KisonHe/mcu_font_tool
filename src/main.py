import fontprocessing
import endprocessing
import os
import os.path
import argparse
import yaml
import jinja2
from jinja2 import Template

languages = []
ids = []
fonts = []
language_strs = []
font_ptrs = []
font_strs = []
default_lang = ""

def font_name_to_font_str(fontname:str)->str:
    fontstr = "font_"+fontname.replace("-", "_").lower()# is spiffs case sensitive?
    return fontstr

def font_str_to_font_ptr(fontstr:str)->str:
    fontptr = fontstr+"_ptr"
    return fontptr


if __name__ == "__main__":
    # TODO: phase args
    # parser = argparse.ArgumentParser(description="Kison's mcu font tool")
    # parser.add_argument("-c","--config",help="Path of config yaml, default config if not provided",required=False) 
    # parser.add_argument("-t", "--target", help="Path of string yaml",required=True)
    
    # args = parser.parse_args()
    # phase args end
    try:
        pass # TODO: load config.yaml here
    except:
        pass
    
    try:    # load the string yaml
        yaml_path = "/home/kisonhe/githubPrjects/mcu_font_tool/example/strings.yaml" #TODO: Process the path
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
        # generate ids & fonts
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
            pass
        pass # TODO: load config.yaml here
    except:
        pass

    # open h template and save generated header
    try:
        string_template_file = open("example/h_stringtable_template.inja","r")
        string_template_string = string_template_file.read()
        string_template_file.close()

        template = Template(string_template_string)
        header_render_result = template.render(languages=languages,ids=ids,fonts=fonts)
        # print(header_render_result) #TODO save to file
        pass
    except:
        pass
    
    # language_strs = [
    #     [
    #         "{Language,\"font_ui_ptr\"}",
    #         "{\\uE1FF,\"font_icon_ptr\"}",
    #     ],
    #     [
    #         "{Language,\"font_ui_ptr\"}",
    #         "{\\uE1FF,\"font_icon_ptr\"}",

    #     ]
    # ]
    # language_strs = []
    try: #generate language_strs
        for lang in string_yaml_dict["Languages"]: # outer loop
            # {'ID': 'Language',
            # 'Content-English': {'Font': 'ui', 'Value': 'Language'},
            # 'Content-Chinese': {'Font': 'ui-25', 'Value': '语言'}}
            strlist = []
            for text in string_yaml_dict["Strings"]:
                liststr = "{\""
                if ("Content-"+lang) in text:
                    liststr=liststr+text["Content-"+lang]["Value"]+"\", "
                    liststr=liststr+font_str_to_font_ptr(font_name_to_font_str(text["Content-"+lang]["Font"]))
                    liststr=liststr+"}"
                elif ("Content-all") in text:
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
        string_template_file = open("example/c_stringtable_template.inja","r")
        string_template_string = string_template_file.read()
        string_template_file.close()

        template = Template(string_template_string)
        # ids = []
        # fonts = []
        # language_strs = {}
        # font_ptrs = []
        # font_strs = []
        c_render_result = template.render(font_ptrs=font_ptrs,default_lang=default_lang,language_strs=language_strs,font_strs=font_strs)
        print(c_render_result) #TODO save to file
        pass
    except:
        pass



