import re
import os
import json

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
        self.classes = {}
        if file != None:
            self.parseString(file)

    def __str__(self):
        return "\nStylesheet with classes:\n{0}".format(json.dumps(self.classes))

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
            tclass = {}
            for y in ta.split(";"):
                z = y.split(":")
                if len(z) > 1:
                    tclass[str(z[0])] = str(z[1])
            self.classes[tc] = tclass

        if debugMode >= 1: print("[PUIL_DEBUG] Done parsing string")
        if debugMode == 2: print("[PUIL_DEBUG] Result:{0}".format(str(self)))

        return (self, classNames, classesData, parsestring)

    def parseFile(self, f):
        with open(f, "r", encoding="utf-8") as file:
            return self.parseString(file.read())

debugMode = 0
if debugMode >= 1: print("[PUIL_DEBUG] Loading default classes")
defaultSheet = Stylesheet()
defaultSheet.parseFile("./defaults.css")

def speedtest():
    import sys
    def flush():
        sys.stdout.flush()

    print("Starting speed&memory tests...")
    flush()
    import psutil, time
    debugMode = 0
    print("Starting test 1 - 1 Large CSS File")
    flush()

    test1memorystart = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    test1timestart = time.time()

    ts = Stylesheet()
    ts.parseFile("./huge.css")

    test1timeend = time.time()
    test1memoryend = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("Test 1 done! Starting test 2 - 100 Large CSS Files")
    flush()

    test2memorystart = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    test2timestart = time.time()

    temparray = []
    for x in range(100):
        s = Stylesheet()
        s.parseFile("./huge.css")
        temparray.append(s)

    test2timeend = time.time()
    test2memoryend = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("Test 2 done! Starting Test 3 - Defaults.css")
    flush()

    test3memorystart = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    test3timestart = time.time()

    ds = Stylesheet()
    ds.parseFile("./defaults.css")

    test3timeend = time.time()
    test3memoryend = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("Test 3 done! Starting Test 4 - Defaults.css 100 times")
    flush()

    test4memorystart = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    test4timestart = time.time()

    temparray2 = []
    for x in range(100):
        s = Stylesheet()
        s.parseFile("./defaults.css")
        temparray2.append(s)

    test4timeend = time.time()
    test4memoryend = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)


    print("All tests done! Results:\n{0}".format(
        "Test 1 - Large CSS File:\n\tTime (seconds): " +
        str(test1timeend - test1timestart) +
        "\n\tMemory usage after test (MegaBytes): " +
        str(test1memoryend - test1memorystart) +
        "\nTest 2 - 100 Large CSS Files:\n\tTime (seconds): " +
        str(test2timeend - test2timestart) +
        "\n\tMemory usage after test (MegaBytes): " +
        str(test2memoryend - test2memorystart) +
        "\nTest 3 - Defaults.css:\n\tTime (seconds): " +
        str(test3timeend - test3timestart) +
        "\n\tMemory usage after test (MegaBytes): " +
        str(test3memoryend - test3memorystart) +
        "\nTest 4 - Defaults.css 100 times:\n\tTime (seconds): " +
        str(test4timeend - test4timestart) +
        "\n\tMemory usage after test (MegaBytes): " +
        str(test4memoryend - test4memorystart)
    ))

def debug():
    global debugMode
    debugMode = 2
    ts = Stylesheet()
    ts.parseFile("./defaults.css")
    print(ts.classes)

if __name__ == "__main__":
    inp = input("Select what you want to do:\n  1: SpeedTest\n  2. Debug\n  3: exit\n> ")
    if inp == "1":
        speedtest()
    elif inp == "2":
        debug()
    else:
        pass
