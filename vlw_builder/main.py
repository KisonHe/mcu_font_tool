import time
import os
import os.path
import pathlib
# just read all chars in the cpp file and out out them.
# it is ezer to write right?


# path to the cpp file containing strings
# cpp_path = "src/Kstrings.cpp"
cpp_path_relative = True
cpp_path = "example/Kstrings.cpp"

# better use relative ones
PDEFileFolder_path_relative = True
#! Note
# Sketch name must same as parent folder, just like arduino
# example, your folder is Create_font, then your file should be Create_font/Create_font.pde
PDEFileFolder_path = "Create_font"
PDEJava_path_relative = False
PDEJava_path = "/your_install_path/processing-version/processing-java"

cpppath = cpp_path
PDEFileFolderpath = PDEFileFolder_path
PDEJavapath = PDEJava_path

my_path = os.path.abspath(os.path.dirname(__file__))

if (cpp_path_relative):
    cpppath = os.path.join(my_path, cpp_path)
    pass

if (PDEFileFolder_path_relative):
    PDEFileFolderpath = os.path.join(my_path, PDEFileFolder_path)
    pass

if (PDEJava_path_relative):
    PDEJavapath = os.path.join(my_path, PDEJava_path)
    pass

tmp = pathlib.PurePosixPath(PDEFileFolderpath)
p = tmp.parents
PDEFileName = PDEFileFolderpath.replace(str(p[0]),"")
PDEFilepath = PDEFileFolderpath + PDEFileName + ".pde"


try:
    CPPfin = open(cpppath,"r")
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,:
    print('Fail to open cpp file')
    # time.sleep(1)
    os._exit(1)

readStr = CPPfin.read()
CPPfin.close()

unicodeList = []

for i in readStr:
    if (not i.isspace()):
        if (ord(i) not in unicodeList):
            unicodeList.append(ord(i))

replacementText = "\nstatic final int[] specificUnicodes = {\n"
for i in unicodeList:
    replacementText = replacementText + str(i) + ", "
    pass
replacementText = replacementText[0:-2]
replacementText = replacementText + "\n};\n"
# print(replacementText)
# print(len(unicodeList))
# print(unicodeList)

os.system("cp " + PDEFilepath + " " + PDEFilepath + ".old")

try:
    PDEFilefin = open(PDEFilepath,"r")
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,:
    print('Fail to open pde file')
    # time.sleep(1)
    os._exit(1)
    pass

readStr = PDEFilefin.read()

PDEFilefin.close()

delimeterA = "//>>specificUnicodes Start"
delimeterB = "//>>specificUnicodes end"

leadingText = readStr.split(delimeterA)[0]
trailingText = readStr.split(delimeterB)[1]

newStr = leadingText + delimeterA + replacementText + delimeterB + trailingText
# print(newStr)

try:
    PDEFilefin = open(PDEFilepath,"w")
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,:
    print('Fail to open pde file as write')
    # time.sleep(1)
    os._exit(1)
    pass

PDEFilefin.write(newStr)
PDEFilefin.close()
print('PDE file wrote')

print("running pde...")
# os.system(PDEJavapath + " --sketch=" + PDEFileFolderpath.split("/")[0] + " --run")
# result = os.popen('cat /etc/services').read()
os.system(PDEJavapath + " --sketch=" + PDEFileFolderpath + " --run")
