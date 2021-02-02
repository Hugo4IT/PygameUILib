import re
import os

try:
    debugMode = 2 if os.environ["PUIL_DEBUG"] == "FULL" else 1
except:
    debugMode = 0

def getAllCharsBetween(string, f, to):
    result = []
    amount = amount1 = string.count(f)
    amount2 = string.count(to)
    if amount1 > amount2: amount = amount2
    if f == to: amount/=2
    for x in range(amount):
        if to in string.split(f)[x+1]: result.append(string.split(f)[x+1].split(to)[0])
    return result

class StyleClass:
    def __init__(self, cname):
        self.className = cname
        self.attributes = {}
    def __str__(self):
        return "Class name: {0}\nData:{1}\n".format(self.className, self.attributes)

class Stylesheet:
    def __init__(self, file = None):
        self.classes = []
        if file != None:
            self.parseString(file)

    def __str__(self):
        tc = ""
        for x in self.classes:
            tc += "\n"
            tc += str(x)
        return "Stylesheet with classes:\n{0}".format(tc)

    def parseString(self, pstr):
        if debugMode == 2: print("[PUIL_DEBUG] Parsing String\n{0}".format(pstr))
        elif debugMode == 1: print("[PUIL_DEBUG] Parsing String...")
        parsestring = pstr
        if debugMode >= 1: print("[PUIL_DEBUG] Removing whitespace...")
        parsestring = parsestring.replace(" ", "")
        parsestring = parsestring.replace("\t", "")
        parsestring = parsestring.replace("\n", "")
        if debugMode >= 1: print("[PUIL_DEBUG] Removed whitespace, result:")
        if debugMode == 2: print(parsestring)
        if debugMode >= 1: print("[PUIL_DEBUG] Removing comments...")
        comments = r"\/\*(.*?)\*\/"
        parsestring = re.sub(comments, "", parsestring)
        if debugMode == 2: print("[PUIL_DEBUG] Removed comments from string, result:\n{0}".format(parsestring))
        if debugMode >= 1: print("Getting all classes")
        classNames = []
        classNames.append(parsestring.split("{")[0])
        classNames.extend(getAllCharsBetween(parsestring, "}", "{"))
        classesData = getAllCharsBetween(parsestring, "{", "}")
        if debugMode == 2: print("[PUIL_DEBUG] Got all classes, result:\nClassnames:\n{0}\nClassAttributes:\n{1}"
        .format(str(classNames), classesData))
        elif debugMode == 1: print("[PUIL_DEBUG] Got all classes")
        for x in range(len(classNames)):
            tc = classNames[x]
            ta = classesData[x]
            tclass = StyleClass("")
            for y in ta.split(";"):
                type = "default"
                tclass.className = tc
                if ":" in tc:
                    type = tc.split(":")[1]
                    tclass.className = tc.split(":")[0]
                createNew = not type in tclass.attributes
                z = y.split(":")
                if type not in tclass.attributes:
                    tclass.attributes[type] = {}
                if len(z) == 2:
                    tclass.attributes[type][str(z[0])] = str(z[1])
                if createNew:
                    self.classes.append(tclass)
        if debugMode == 2: print("[PUIL_DEBUG] Current ungrouped classes:\n"+str(self))
        if debugMode >= 1: print("[PUIL_DEBUG] Grouping classes")
        namearray = []
        for x in self.classes:
            namearray.append(x.className)
        for x in self.classes:
            samenames = []
            for y in self.classes:
                if ":" in y.className:
                    if y.className.split(":")[0] == x.className:
                        samenames.append(y)
                else:
                    if y.className == x.className:
                        samenames.append(y)
            if len(samenames) >= 2:
                firstclass = samenames[0]
                samenames.pop(0)
                for y in samenames:
                    firstclass.attributes[list(y.attributes.keys())[0]] = y.attributes[list(y.attributes.keys())[0]]
                    self.classes.remove(y)

        if debugMode >= 1: print("[PUIL_DEBUG] Done parsing string")
        if debugMode == 2: print("[PUIL_DEBUG] Result:")
        print(self)
        return (self, classNames, classesData, parsestring)

    def parseFile(self, f):
        with open(f, "r", encoding="utf-8") as file:
            return self.parseString(file.read())

debugMode = 2
if debugMode >= 1: print("[PUIL_DEBUG] Loading default classes")
defaultSheet = Stylesheet()
defaultSheet.parseFile("./defaults.css")

if __name__ == "__main__":
    ts = Stylesheet()
    ts.parseFile("./huge.css")
