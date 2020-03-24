from configobj import ConfigObj
from os.path import isfile
from os import listdir
from locale import getdefaultlocale
IL8N_SETTINGS_PATH = "setting/il8n"
def formatPath(path:str):
    return IL8N_SETTINGS_PATH+"/"+path
def getSysLang():
    return getdefaultlocale()[0]
def readDefaultLangPath():
    default_lang=ConfigObj(formatPath("il8n.ini"),encoding="utf-8")
    default_lang=default_lang["default"]["default_lang"]
    return formatPath(default_lang)
def getSysDefualtINIPath():
    n=formatPath(getSysLang()+".ini")

    if not isfile(n) or ConfigObj(formatPath("il8n.ini"),encoding="utf-8")["default"]["is_use_sys_default"] == "0":
        return readDefaultLangPath()
    else:
        return n
class Il8n(object):
    def __init__(self,file_path=getSysDefualtINIPath()):
        self.path=file_path
        self.config_obj=ConfigObj(file_path,encoding="utf-8")
    def getAuthor(self):
        return self.config_obj["meta"]["author"]
    def getName(self):
        return self.config_obj["meta"]["name"]
    def getDesc(self):
        return self.config_obj["meta"]["desc"]
    def getVersion(self):
        return self.config_obj["meta"]["version"]
    def _(self,label):
        return self.config_obj["mainWindow"][label]
    def __str__(self):
        return "%s"%self.path
    def __repr__(self):
        return "<il8n:%s>"%self.path

def getAllIL8N():
    d=listdir(IL8N_SETTINGS_PATH)
    d2=d[:]

    for i in d:
        if not isfile(formatPath(i)):
            d2.remove(i)
            continue
        elif i == "il8n.ini":
            d2.remove(i)
            continue
        ind=int(d2.index(i))
        d2[ind]=Il8n(IL8N_SETTINGS_PATH+"/"+i)
    return d2
print(getAllIL8N())