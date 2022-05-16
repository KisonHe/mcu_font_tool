import jinja2
from jinja2 import Template
string_template_file = open("./test/strings_template.inja","r")
string_template_string = string_template_file.read()
string_template_file.close()

template = Template(string_template_string)
print(template.render(languages={"a","b"}))