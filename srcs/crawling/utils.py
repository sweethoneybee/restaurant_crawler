import time


def logging(*msg):
    f = open("../../log/crawlingLog.txt", "a")

    if msg == None:
        data = time.strftime('%c', time.localtime(
            time.time())) + " 로그 정보가 넘어오지 않았습니다\n"
        f.write(data)
        f.close()
        return

    data = ""
    for word in msg:
        data += word
        data += " "

    data += "\n"
    f.write(data)
    f.close()
    return


def saveCrawlIndex(index):
    data = index
    if type(data) is int:
        data = str(data)

    f = open("../../log/crawlEndIndex.txt", "w")
    f.write(data)
    f.close()


def readCrawlIndex():
    f = open("../../log/crawlEndIndex.txt", "r")
    data = f.read()
    if type(data) is str:
        data = int(data)
    data += 1
    return data


def saveFilename(name):
    if name == None:
        return

    f = open("../../filename/filename", "a")
    data = name + ".json "
    f.write(data)
    f.close()
    return
