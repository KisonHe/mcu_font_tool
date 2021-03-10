#!/usr/bin/python3
import sys
import argparse
import yaml

fontA = 1
fontB = 1

# example of fontDict
var = {
    #   
        fontA : {"languageA":["str1","str2"],"languageB":["str1","str2"]},
        fontB : {"languageA":["str1"],"languageB":["str2","str3"]},
    }

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



def modifyPDE(file:dict())->list():
    unicodeBlockStr = ""
    fontNumberStr = ""
    specificUnicodesStr = ""
    # if (args.jpg):
    #         pass #TODO make this feature
    for f in fonts:
        unicodeBlockStr = ""
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

    replacementText = "\nstatic final int[] specificUnicodes = {\n"
    for i in unicodeList:
        replacementText = replacementText + str(i) + ", "
        pass
    replacementText = replacementText[0:-2]
    replacementText = replacementText + "\n};\n"
    print(replacementText)
    return [fontNumberStr,unicodeBlockStr,specificUnicodesStr]






if (__name__ == "__main__"):
    with open("/home/kisonhe/githubPrjects/TFT_eSPI_Assi/vlw_builder/config.yaml", 'r') as stream:
        try: 
            file = yaml.safe_load(stream)
            updateSourceFiles(file)
            modifyPDE(file)
            # print(names)
            # print(languages)
            # getInfoFromYaml(file)
            # print(file)
            # print(file["Strings"][0])
            # print(type(file))
        except yaml.YAMLError as exc:
            print(exc)
