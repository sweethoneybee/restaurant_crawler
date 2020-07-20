import json


def readJsonFile(filepath):
    f = open(filepath, "r")
    jsonData = json.load(f)
    f.close()
    return jsonData
