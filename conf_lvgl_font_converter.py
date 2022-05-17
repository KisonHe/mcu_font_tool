from conf_font_converter import conf_font_converter_t

class conf_lvgl_font_converter_t(conf_font_converter_t):
    def init_values(self):
        # init values
        self.output = "bin"
        self.converter_command = "lv_font_conv"
        self.subpx = "None"
        self.upload_command = ""
        self.source_path = "../mcu_font_config"
        self.template_path = "../mcu_font_template"
        self.gen_bash_path = "./scripts"
        self.output_path = "../../src/gui"

    def __init__(self) -> None:
        super().__init__()
        self.init_values()
        pass

    def load_settings_from_yaml(self,yamldict:dict,args)->int:
        if (not "Type" in yamldict) or (yamldict["Type"]!="lvgl"):
            return -1
        if ("OutPut" in yamldict):
            self.output = yamldict["OutPut"]
            pass
        if ("Command" in yamldict):
            self.converter_command = yamldict["Command"]
            pass
        if ("Subpixel" in yamldict):
            self.subpx = yamldict["Subpixel"]
            pass
        if ("UploadCommand" in yamldict):
            self.upload_command = yamldict["UploadCommand"]
            pass
        if ("SourcePath" in yamldict):
            self.SourcePath = yamldict["UploadCommand"]
            pass
        return 0
