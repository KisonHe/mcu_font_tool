#!/usr/bin/python3

import time
import os
import os.path
import pathlib
import contextlib
import argparse
import yaml
# ask if to create kstrings.cpp and .h if doesn't exist

# Note: SPIFFS does NOT accept underscore in a filename!
#       If font name has underscore, better change it manually
# Note: If you need to format print to string then show it, 
#       You SHOULD handle this by ADDING EXTRA ExtraBlock
#       in the config.yaml 
# Note: It is your job to make sure string declared to use font a,
#       is not actually using font b in the tft lib

#      >>>>>>>>>> USER CONFIGURED PARAMETERS START HERE <<<<<<<<<<

global data_folder_path_relative
global data_folder_path
global h_path_relative
global h_path
global cpp_path_relative 
global cpp_path
global PDEFileFolder_path_relative 
global PDEFileFolder_path
global PDEJava_path_relative
global PDEJava_path
global file 
global cpppath 
global hpath 
global PDEFileFolderpath 
global PDEJavapath 
global my_path 
global fonts 
global fontDict 
global names 
global languages 
global yaml_path_relative
global yaml_path

data_folder_path_relative = True
data_folder_path = "../data"


yaml_path_relative = True
yaml_path = "config.yaml"

# Note: path to the .h file containing strings
h_path_relative = True
h_path = "example/Kstrings.h"

# Note: path to the .cpp file containing strings
cpp_path_relative = True
cpp_path = "example/Kstrings.cpp"

# Note: Sketch name must same as parent folder, just like arduino
#       example, your folder is Create_font, then your file should be Create_font/Create_font.pde
PDEFileFolder_path_relative = True
PDEFileFolder_path = "Create_font"

PDEJava_path_relative = False
PDEJava_path = "~/git_install_software/processing-3.5.4/processing-java"


#      >>>>>>>>>> USER CONFIGURED PARAMETERS END HERE <<<<<<<<<<

# global vars
file = ""
cpppath = ""
hpath = ""
PDEFileFolderpath = ""
PDEJavapath = ""
my_path = ""
PDEFilepath = ""
fonts = []
fontDict = {}
names = []
languages = []

def getAllFonts(file:dict):
    for i in file["Fonts"]:
        fonts.append(i["Name"])
        pass
    pass

def getAllLanguages(file:dict):
    for i in file["Languages"]:
        languages.append(i)
        pass
    pass


def getAllNames(file:dict):
    for i in file["Strings"]:
        names.append(i["Name"])
        pass
    pass

def getInfoFromYaml(file:dict):
    getAllNames(file)
    pass

def updateSourceFiles(file:dict())->list():
    replaceTextCpp = ""
    replaceTextH = ""
    getAllLanguages(file)
    getAllNames(file)
    getAllFonts(file)

    # generate fontdict
    for f in fonts:
        tmpdict_2 = {}
        for l in languages:
            tmplist_2 = []
            for i in file["Strings"]:
                if ("Content-" + l in i):   # over-write in specific language
                    if (f == i["Content-" + l]["Font"]):
                        tmplist_2.append(i["Content-" + l]["Value"])
                        pass
                    pass
                elif ("Content-all" in i):
                    if (f == i["Content-all"]["Font"]):
                        tmplist_2.append(i["Content-all"]["Value"])
                        pass
                    pass
                pass
            tmpdict_2[l] = tmplist_2
            pass
        fontDict[f] = tmpdict_2
        pass
    # generate Names enum
    replaceTextH = replaceTextH + "enum Names{"
    for n in names:
        replaceTextH = replaceTextH + n + ", "
        pass
    replaceTextH = replaceTextH[0:-2]   # get rid of last ', '
    replaceTextH = replaceTextH + "};\n"

    # generate Languages enum
    replaceTextH = replaceTextH + "enum Languages{"
    for l in languages:
        replaceTextH = replaceTextH + l + ", "
        pass
    replaceTextH = replaceTextH[0:-2]   # get rid of last ', '
    replaceTextH = replaceTextH + "};\n"

    tmplist = []
    for l in languages:
        replaceTextCpp = replaceTextCpp + "const char* " + l + "Strings[] = {"
        for f in fontDict:
            for tmpstr in fontDict[f][l]:
                replaceTextCpp = replaceTextCpp + "\"" + tmpstr + "\"" + ", "
                pass
            pass
        if (replaceTextCpp.endswith(", ")): # incase first languages have no strings added at all
            replaceTextCpp = replaceTextCpp[0:-2]
            replaceTextCpp = replaceTextCpp + "};\n"
            pass

    return [replaceTextCpp,replaceTextH]
    pass


# process user defined path to useable path
def getFilesPaths():
    global data_folder_path_relative ,data_folder_path ,h_path_relative ,h_path ,cpp_path_relative  ,cpp_path ,PDEFileFolder_path_relative  ,PDEFileFolder_path ,PDEJava_path_relative ,PDEJava_path ,file  ,cpppath  ,hpath  ,PDEFileFolderpath  ,PDEJavapath  ,my_path  ,fonts  ,fontDict  ,names  ,languages 
    global yaml_path_relative
    global yaml_path
    global PDEFilepath
    my_path = os.path.abspath(os.path.dirname(__file__))
    cpppath = cpp_path
    PDEFileFolderpath = PDEFileFolder_path
    PDEJavapath = PDEJava_path

    if (yaml_path_relative):
        yaml_path = str(pathlib.Path(os.path.join(my_path,yaml_path)).resolve())
        pass

    if (data_folder_path_relative):
        data_folder_path = str(pathlib.Path(os.path.join(my_path,data_folder_path)).resolve())
        pass

    if (cpp_path_relative):
        cpppath = str(pathlib.Path(os.path.join(my_path,cpp_path)).resolve())
        pass

    if (h_path_relative):
        hpath = str(pathlib.Path(os.path.join(my_path,h_path)).resolve())
        pass

    if (PDEFileFolder_path_relative):
        PDEFileFolderpath = str(pathlib.Path(os.path.join(my_path,PDEFileFolder_path)).resolve())
        pass

    if (PDEJava_path_relative):
        PDEJavapath = str(pathlib.Path(os.path.join(my_path,PDEJava_path)).resolve())
        pass

    tmp = pathlib.PurePosixPath(PDEFileFolderpath)
    p = tmp.parents
    PDEFileName = PDEFileFolderpath.replace(str(p[0]),"")
    PDEFilepath = PDEFileFolderpath + PDEFileName + ".pde"
    pass


def getPDEStr(f:str,file:dict())->list():
    unicodeBlockStr = ""
    fontNumberStr = ""
    specificUnicodesStr = ""
    # if (args.jpg):
    #         pass #TODO make this feature
    # for f in fonts:
    for f2 in file["Fonts"]:
        if ("ExtraBlock" in f2):
            unicodeBlockStr = unicodeBlockStr + f2["ExtraBlock"]
            pass
        else:
            unicodeBlockStr = ""
        if ("TTF-Num" in f2):
            fontNumberStr = "\nint fontNumber = " + str(f2["TTF-Num"]) + ";\n" + "String fontName = \"Final-Frontier\";\n"
            pass
        elif ("TTF-Name" in f2):
            fontNumberStr = "\nint fontNumber = -1;\n" + "String fontName = \"" + f2["TTF-Name"] + "\";\n"
            pass
        else:
            raise ValueError("Missing TTF-Name or TTF-Num")
        fontNumberStr = fontNumberStr + "String fontType = \".ttf\";\nint fontSize = " + str(f2["Size"]) + ";\nint displayFontSize = " + str(f2["Size"]) + ";"
        print(fontNumberStr)
        pass
        # pass
    
    allStrs = []
    tmplist_3 = []
    for f in fontDict:
        tmpdict = fontDict[f] 
        for l in languages:
            tmplist_3 = tmplist_3 + tmpdict[l]
            pass
        pass
    for s in tmplist_3:
        if (not s in allStrs):
            allStrs.append(s)
            pass
        pass
    unicodeList = []

    for s in allStrs:
        for c in s:
            if (not c.isspace()):
                if (ord(c) not in unicodeList):
                    unicodeList.append(ord(c))    
                    pass
                pass
            pass
        pass

    specificUnicodesStr = "\nstatic final int[] specificUnicodes = {\n"
    for i in unicodeList:
        specificUnicodesStr = specificUnicodesStr + str(i) + ", "
        pass
    specificUnicodesStr = specificUnicodesStr[0:-2]
    specificUnicodesStr = specificUnicodesStr + "\n};\n"

    unicodeBlockStr = "\nstatic final int[] unicodeBlocks = {\n" + unicodeBlockStr + "\n};\n"
    # print(replacementText)
    return [fontNumberStr,unicodeBlockStr,specificUnicodesStr]






if (__name__ == "__main__"):
    # Note:
    # because yaml file has infomation like ExtraBlock
    # it is easier to require update from yaml when
    # generating vlw files
    parser = argparse.ArgumentParser(description="Help to generate vlw files for TFT_eSPI lib")
    actiongroup = parser.add_mutually_exclusive_group(required=True)
    actiongroup.add_argument("-a", "--all", help="Do all the stuff, will copy vlw to data folder",action="store_true")
    actiongroup.add_argument("-y", "--yaml", help="Transfer yaml to source files only",action="store_true")
    parser.add_argument("-j","--jpg",help="save jpg file to check created fonts",action="store_true",required=False)   #TODO: need to modify .pde file
    args = parser.parse_args()
    if (args.all):
        #balabala
        pass
    elif (args.yaml):
        pass
    else:
        print("How did we get here???")
        os._exit(1)
        pass

    getFilesPaths()

    if (args.all or args.yaml):
        try:
            os.system("cp " + cpppath + " " + cpppath + ".old")
            os.system("cp " + hpath + " " + hpath + ".old")
            CPPfin = open(cpppath,"r")
            readStr = CPPfin.read()
            CPPfin.close()
            stream = open(yaml_path, 'r')
            file = yaml.safe_load(stream)
            [cstr,hstr] = updateSourceFiles(file)
            # write .cpp file
            delimeterA = "//>>KstringsCPP Start"
            delimeterB = "//>>KstringsCPP End"
            leadingText = readStr.split(delimeterA)[0]
            trailingText = readStr.split(delimeterB)[1]
            newStr = leadingText + delimeterA + "\n" + cstr + delimeterB + trailingText
            CPPfin = open(cpppath,"w")
            CPPfin.write(newStr)
            CPPfin.close()

            # write .h file
            Hfin = open(hpath,"r")
            readStr = Hfin.read()
            Hfin.close()
            delimeterA = "//>>KstringsH Start"
            delimeterB = "//>>KstringsH End"
            leadingText = readStr.split(delimeterA)[0]
            trailingText = readStr.split(delimeterB)[1]
            newStr = leadingText + delimeterA + "\n" + hstr + delimeterB + trailingText
            Hfin = open(hpath,"w")
            Hfin.write(newStr)
            Hfin.close()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,:
            # time.sleep(1)
            os._exit(1)
            pass
        # prepare to do cpp files
        pass

    if (args.all):
        for font in fonts:
            os.system("cp " + PDEFilepath + " " + PDEFilepath + ".old")
            PDEFilefin = open(PDEFilepath,"r")
            readStr = PDEFilefin.read()
            PDEFilefin.close()

            # modify pde file
            [fstr,bstr,ustr] = getPDEStr(font,file)
            delimeterA = "//>>fontNumber Start"
            delimeterB = "//>>fontNumber End"
            leadingText = readStr.split(delimeterA)[0]
            trailingText = readStr.split(delimeterB)[1]
            newStr = leadingText + delimeterA + fstr + delimeterB + trailingText

            delimeterA = "//>>unicodeBlocks Start"
            delimeterB = "//>>unicodeBlocks End"
            leadingText = newStr.split(delimeterA)[0]
            trailingText = newStr.split(delimeterB)[1]
            newStr = leadingText + delimeterA + bstr + delimeterB + trailingText

            delimeterA = "//>>specificUnicodes Start"
            delimeterB = "//>>specificUnicodes End"
            leadingText = newStr.split(delimeterA)[0]
            trailingText = newStr.split(delimeterB)[1]
            newStr = leadingText + delimeterA + ustr + delimeterB + trailingText

            PDEFilefin = open(PDEFilepath,"w")
            PDEFilefin.write(newStr)
            PDEFilefin.close()
            print('PDE file wrote ' + font)
            print("running pde for " + font + " ...")

        # print(newStr)
        try:
            pass
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,:
            # time.sleep(1)
            os._exit(1)
            pass







    

    # unicodeList = []

    # for i in readStr:
    #     if (not i.isspace()):
    #         if (ord(i) not in unicodeList):
    #             unicodeList.append(ord(i))

    # replacementText = "\nstatic final int[] specificUnicodes = {\n"
    # for i in unicodeList:
    #     replacementText = replacementText + str(i) + ", "
    #     pass
    # replacementText = replacementText[0:-2]
    # replacementText = replacementText + "\n};\n"
    # # print(replacementText)
    # # print(len(unicodeList))
    # # print(unicodeList)

    # os.system("cp " + PDEFilepath + " " + PDEFilepath + ".old")

    # try:
    #     PDEFilefin = open(PDEFilepath,"r")
    # except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst)          # __str__ allows args to be printed directly,:
    #     print('Fail to open pde file')
    #     # time.sleep(1)
    #     os._exit(1)
    #     pass

    # readStr = PDEFilefin.read()

    # PDEFilefin.close()

    # delimeterA = "//>>specificUnicodes Start"
    # delimeterB = "//>>specificUnicodes end"

    # leadingText = readStr.split(delimeterA)[0]
    # trailingText = readStr.split(delimeterB)[1]

    # newStr = leadingText + delimeterA + replacementText + delimeterB + trailingText
    # # print(newStr)

    # try:
    #     PDEFilefin = open(PDEFilepath,"w")
    # except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst)          # __str__ allows args to be printed directly,:
    #     print('Fail to open pde file as write')
    #     # time.sleep(1)
    #     os._exit(1)
    #     pass

    # PDEFilefin.write(newStr)
    # PDEFilefin.close()
    # print('PDE file wrote')

    # print("running pde...")
    # # os.system(PDEJavapath + " --sketch=" + PDEFileFolderpath.split("/")[0] + " --run")
    # # result = os.popen('cat /etc/services').read()
    # os.system(PDEJavapath + " --sketch=" + PDEFileFolderpath + " --run")
