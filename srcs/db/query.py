import pymysql
import requests


def updateDb(conn, curs):
    f = open('../../filename/filename', 'r')
    filename = f.read()
    f.close()

    startIndex = 0
    endIndex = 0
    fpath = ""
    for name in filename:
        if(name == ' '):
            fpath = filename[startIndex:endIndex]
            fpath = "../../restaurant_json/" + fpath

            f = open(fpath, 'r')
            jsonData = f.read()
            f.close()

            insertIntoDatabase(conn, curs, jsonData)
            startIndex = endIndex + 1

        endIndex += 1


def insertIntoDatabase(conn, curs, results):

    for restaurant in results:
        name = restaurant["name"]
        number_of_naver_reviews = restaurant["numberOfNaverReviews"]
        # number_of_google_reviews = restaurant["number_of_google_reviews"]
        open_time = restaurant["openTime"]
        # open_flag = restaurant["open_flag"]
        phone_number = restaurant["tel"]
        latitude = restaurant["lat"]
        longitude = restaurant["lng"]
        # naver_rating = restaurant["naver_rating"]
        # google_rating = restaurant["google_rating"]
        address = restaurant["address"]
        road_address = restaurant["roadAddress"]
        # price_level = restaurant["price_level"]

        # google_id = restaurant["googleId"]
        naver_id = restaurant["naverId"]
        # print(type(name))
        # print(type(number_of_naver_reviews))
        # print(type(open_time))
        # print(type(phone_number))
        # print(type(latitude))
        # print(type(longitude))
        # print(type(address))
        # print(type(road_address))
        # print(type(naver_id))
        # break
        # sql = f"insert into restaurants(name, number_of_naver_reviews, open_time, phone_number, latitude, longitude, address, road_address, naver_id) values ({name}, {number_of_naver_reviews}, {open_time}, {phone_number}, {latitude}, {longitude}, {address}, {road_address}, {naver_id})"
        sql = f'''insert into restaurants(
            name,
            number_of_naver_reviews,
            open_time,
            phone_number,
            latitude,
            longitude,
            address,
            road_address,
            naver_id)
            values ('{name}', '{number_of_naver_reviews}', '{open_time}', '{phone_number}', '{latitude}', '{longitude}', '{address}', '{road_address}', '{naver_id}')'''
        # print(name)
        # sql = f'''insert into restaurants (
        #     name)
        #     values ('{name}')'''
        curs.execute(sql)
        conn.commit()


# name
# number_of_naver_reviews
# open_time
# phone_number
# latitude
# longitude
# address
# road_address
# naver_id
