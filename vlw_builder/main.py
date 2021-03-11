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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# global vars
file = ""
cpppath = ""
hpath = ""
PDEFileFolderpath = ""
PDEJavapath = ""
my_path = ""
PDEFilepath = ""
fonts = []
# example of fontDict
# var = {  
#         fontA : {"languageA":["str1","str2"],"languageB":["str1","str2"]},
#         fontB : {"languageA":["str1"],"languageB":["str2","str3"]},
#     }
fontDict = {}
names = []
languages = []

# replace everything in raw between start-end with str2replace
def replaceStrBetween(raw:str,str2replace:str,start:str,end:str)->str:
    delimeterA = start
    delimeterB = end
    leadingText = raw.split(delimeterA)[0]
    trailingText = raw.split(delimeterB)[1]
    return leadingText + delimeterA + str2replace + delimeterB + trailingText


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
                for lang in languages:
                    if (not (("Content-all" in i) or ("Content-" + lang in i))):
                        raise ValueError(f"{i} lack {lang} translation")
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
    mapAssiList = []
    index = -1
    for l in languages:
        mapAssiList.append([])
        index += 1
        replaceTextCpp = replaceTextCpp + "const char* " + l + "Strings[] = {"
        for f in fontDict:
            for tmpstr in fontDict[f][l]:
                replaceTextCpp = replaceTextCpp + "\"" + tmpstr + "\"" + ", "
                mapAssiList[index].append(f)
                pass
            pass
        if (replaceTextCpp.endswith(", ")): # incase first languages have no strings added at all
            replaceTextCpp = replaceTextCpp[0:-2]
            replaceTextCpp = replaceTextCpp + "};\n"
            pass
    replaceTextCpp = replaceTextCpp + "const char** namelist[] = {"
    for l in languages:
        replaceTextCpp = replaceTextCpp + l + "Strings" + " ,"
        pass
    replaceTextCpp = replaceTextCpp[0:-2]
    replaceTextCpp = replaceTextCpp + "};\n"

    if (os.path.exists(os.path.join(PDEFileFolderpath,"FontFiles/System_Font_List.txt"))):
        txtfin = open(os.path.join(PDEFileFolderpath,"FontFiles/System_Font_List.txt"),"r")
        txtreadStr = txtfin.read()
        txtfin.close()
        for n1,m in enumerate(mapAssiList):
            for n2,m2 in enumerate(mapAssiList[n1]):
                for n3,f in enumerate(file["Fonts"]):
                    if (f["Name"] == m2):
                        # size = f["Size"]
                        # pos = txtreadStr.find(str(f["TTF-Num"])) + len(str(f["TTF-Num"])) + 2
                        # posend = txtreadStr.find("\n",pos)
                        # fontstr = txtreadStr[pos:posend]
                        # fontstr = fontstr.replace(' ','')
                        # fontstr = fontstr.replace('-','')
                        # fontstr = fontstr[len(fontstr) - 20:len(fontstr)]
                        # fontstr = fontstr + str(size)
                        mapAssiList[n1][n2] = n3
                        pass
                        # mapAssiList[n1][n2] = f["TTF-Num"]
                        
                # #在这里直接找txt的name,整合size进去
                # # file["Fonts"][name]
                # txtreadStr.find("123")
                pass
            pass
        languageStr = "uint8_t* map[] = {"
        replaceTextCpp += "const char* Fonts[] = {"
        fontstrlist = []
        for n,f in enumerate(file["Fonts"]):
            size = f["Size"]
            pos = txtreadStr.find(str(f["TTF-Num"])) + len(str(f["TTF-Num"])) + 2
            posend = txtreadStr.find("\n",pos)
            fontstr = txtreadStr[pos:posend]
            fontstr = fontstr.replace(' ','')
            fontstr = fontstr.replace('-','')
            if (len(fontstr) > 20):
                fontstr = fontstr[len(fontstr) - 20:len(fontstr)]
            fontstr = fontstr + str(size)
            replaceTextCpp += ("\"" + fontstr + "\"")
            replaceTextCpp += ", "
            pass
        replaceTextCpp = replaceTextCpp[0:-2]
        replaceTextCpp += "};\n"
        for n1,m in enumerate(mapAssiList):
            replaceTextCpp += "uint8_t "
            replaceTextCpp += (languages[n1] + "map[] = {")
            languageStr += (languages[n1] + "map, ")
            for n2,m2 in enumerate(mapAssiList[n1]):
                replaceTextCpp += str(m2)
                replaceTextCpp += ", "
                pass
            
            replaceTextCpp = replaceTextCpp[0:-2]
            replaceTextCpp += "};\n"
            pass
        languageStr = languageStr[0:-2]
        languageStr += "};\n"
        replaceTextCpp += languageStr
        
        pass

    else:
        print(f"{bcolors.WARNING}Warning: txt not exist, call again{bcolors.ENDC}")
        # todo modify .pde to auto generate txt file

    


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
    fontlist = file["Fonts"]
    for font in fontlist:
        if (font["Name"] == f):
            f2 = font
            break
    if ("ExtraBlock" in f2):
        unicodeBlockStr = unicodeBlockStr + f2["ExtraBlock"]
        pass
    else:
        unicodeBlockStr = ""
    if (("TTF-Num" in f2) and ("TTF-Name" in f2)):
        raise ValueError("TTF-Name, TTF-Num can be only one!")
    if ("TTF-Num" in f2):
        if (type(f2["TTF-Num"]) == type("")):
            print(f"{bcolors.WARNING}Warning: TTF-Num seem to be a string?{bcolors.ENDC}")
        fontNumberStr = "\nint fontNumber = " + str(f2["TTF-Num"]) + ";\n" + "String fontName = \"Final-Frontier\";\n"
        pass
    elif ("TTF-Name" in f2):
        fontNumberStr = "\nint fontNumber = -1;\n" + "String fontName = \"" + f2["TTF-Name"] + "\";\n"
        pass
    else:
        raise ValueError("Missing TTF-Name or TTF-Num")
    fontNumberStr = fontNumberStr + "String fontType = \".ttf\";\nint fontSize = " + str(f2["Size"]) + ";\nint displayFontSize = " + str(f2["Size"]) + ";"
    pass
    
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
    actiongroup.add_argument("-c","--clean",help="Clean vlw file in pde & data folder",action="store_true",required=False) 
    args = parser.parse_args()
    if (args.all):
        #balabala
        pass
    elif (args.yaml):
        pass
    elif (args.clean):
        pass
    else:
        print("How did we get here???")
        os._exit(1)
        pass

    getFilesPaths()

    if (args.clean):
        try:
            os.system("rm " + data_folder_path + "/" + "*.vlw")
        except:
            pass
        try:
            os.system("rm " + os.path.join(PDEFileFolderpath,"FontFiles") + "/" + "*.vlw")
        except:
            pass
        os._exit(0)

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
            newStr = replaceStrBetween(readStr,"\n" + cstr,"//>>KstringsCPP Start","//>>KstringsCPP End")
            CPPfin = open(cpppath,"w")
            CPPfin.write(newStr)
            CPPfin.flush()
            CPPfin.close()
            # time.sleep(3)

            # write .h file
            Hfin = open(hpath,"r")
            readStr = Hfin.read()
            Hfin.close()
            newStr = replaceStrBetween(readStr,"\n" + hstr,"//>>KstringsH Start","//>>KstringsH End")
            Hfin = open(hpath,"w")
            Hfin.write(newStr)
            Hfin.flush()
            Hfin.close()
            # time.sleep(3) 

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
            newStr = replaceStrBetween(readStr,fstr,"//>>fontNumber Start","//>>fontNumber End")
            newStr = replaceStrBetween(newStr,bstr,"//>>unicodeBlocks Start","//>>unicodeBlocks End")
            newStr = replaceStrBetween(newStr,ustr,"//>>specificUnicodes Start","//>>specificUnicodes End")

            PDEFilefin = open(PDEFilepath,"w")
            PDEFilefin.write(newStr)
            PDEFilefin.flush()
            PDEFilefin.close()
            # time.sleep(3) 
            print('PDE file wrote ' + font)
            print("running pde for " + font + " ...")
            os.system(PDEJavapath + " --sketch=" + PDEFileFolderpath + " --run")

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
        pass
    print("Finished Generating. Copying to data folder...")
    os.system("cp " + os.path.join(PDEFileFolderpath,"FontFiles") + "/" + "*.vlw " + data_folder_path)
