import pymysql
import query
import json

conn = pymysql.connect(host='recoderdbinstance.crnm0s8emitk.ap-northeast-2.rds.amazonaws.com',
                       user='recoder', password='shdudtka123', db='sprint1', charset='utf8')
curs = conn.cursor()

fpath = "../../restaurant_json/마포구_합정동.json"
f = open(fpath, "r")
data_string = f.read()
data = json.loads(data_string)
f.close()

query.insertIntoDatabase(conn, curs, data)

# f = open("../../filename/filename", "r")
# f = open('../../filename/filename', 'r')
# filename = f.read()
# f.close()

# startIndex = 0
# endIndex = 0

# for name in filename:
#     if(name == ' '):
#         fpath = filename[startIndex:endIndex]

#         print(fpath)
#         f.close()
#         startIndex = endIndex + 1

#     endIndex += 1
