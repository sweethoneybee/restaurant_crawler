
f = open('../../filename/filename', 'r')
temp = f.read()

f.close()

i = 0
start = 0
end = 0
dataName = ""
for t in temp:
    if(t == ' '):
        dataName = temp[start:end]
        start = end + 1

        print(dataName)
        fpath = "../../restaurant_json/" + dataName
        fileTemp = open(fpath)
        # dataTemp = fileTemp.readline()
        # print(dataTemp)
        fileTemp.close()

    end += 1


def ():
    f = open('../../filename/filename', 'r')
    file = f.read()

    f.close()
