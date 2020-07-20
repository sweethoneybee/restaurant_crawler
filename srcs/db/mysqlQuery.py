import pymysql
import requests
import json
import utils


def insertIntoRestaurant(curs, results):
    for restaurant in results:
        # 단란주점 혹은 호두과자 등 식당에 부적합 데이터 거르기
        metaCategory = restaurant["metaCategory"]
        if metaCategory == None:
            continue

        restaurant_id = restaurant["rId"]
        name = restaurant["name"]
        naver_review_count = restaurant["numberOfNaverReviews"]
        opening_hours = restaurant["openTime"]
        phone_number = restaurant["tel"]
        latitude = restaurant["lat"]
        longitude = restaurant["lng"]
        address = restaurant["address"]
        road_address = restaurant["roadAddress"]
        naver_id = restaurant["naverId"]

        sql = f'''insert into restaurant(
            restaurant_id,
            name,
            naver_review_count,
            opening_hours,
            phone_number,
            latitude,
            longitude,
            address,
            road_address,
            naver_id)
            values ('{restaurant_id}', '{name}', '{naver_review_count}', '{opening_hours}', '{phone_number}', '{latitude}', '{longitude}', '{address}', '{road_address}', '{naver_id}')'''

        curs.execute(sql)


def categoryQrySelect(qryIndex, restaurant_id):
    qry = [
        f"insert into restaurant_category (category_id, restaurant_id) values (1,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (2,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (3,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (4,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (5,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (6,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (7,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (8,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (9,  '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (10, '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (11, '{restaurant_id}');",
        f"insert into restaurant_category (category_id, restaurant_id) values (12, '{restaurant_id}');"]

    return qry[qryIndex]


def insertIntoRestaurantCategory(curs, data):

    for restaurant in data:
        qrySentences = []
        qryIndex = []
        rId = restaurant["rId"]
        for cat in restaurant["metaCategory"]:
            if cat == "한식":
                qryIndex.append(0)
            elif cat == "중식":
                qryIndex.append(1)
            elif cat == "일식":
                qryIndex.append(2)
            elif cat == "양식":
                qryIndex.append(3)
            elif cat == "고기":
                qryIndex.append(4)
            elif cat == "주점":
                qryIndex.append(5)
            elif cat == "카페":
                qryIndex.append(6)
            elif cat == "분식":
                qryIndex.append(7)
            elif cat == "세계음식":
                qryIndex.append(8)
            elif cat == "패스트푸드":
                qryIndex.append(9)
            elif cat == "치킨":
                qryIndex.append(10)
            elif cat == "기타":
                qryIndex.append(11)

        if len(qryIndex) >= 2 and qryIndex[0] != qryIndex[1]:
            qrySentences.append(categoryQrySelect(qryIndex[1], rId))
        qrySentences.append(categoryQrySelect(qryIndex[0], rId))

        for qry in qrySentences:
            curs.execute(qry)


def insertIntoCategory(curs):
    qrySentences = [
        "insert into category(category_id, name) values(1, '한식')",
        "insert into category(category_id, name) values(2, '중식')",
        "insert into category(category_id, name) values(3, '일식')",
        "insert into category(category_id, name) values(4, '양식')",
        "insert into category(category_id, name) values(5, '고기')",
        "insert into category(category_id, name) values(6, '주점')",
        "insert into category(category_id, name) values(7, '카페')",
        "insert into category(category_id, name) values(8, '분식')",
        "insert into category(category_id, name) values(9, '세계음식')",
        "insert into category(category_id, name) values(10, '패스트푸드')",
        "insert into category(category_id, name) values(11, '치킨')",
        "insert into category(category_id, name) values(12, '기타')"]
    for qry in qrySentences:
        curs.execute(qry)


def insertIntoRestaurantPhoto(curs, data):
    for restaurant in data:
        rId = restaurant["rId"]
        path = restaurant["thumUrl"]
        # 없을경우 임시 주소
        if path == None:
            path = "https://cdn.pixabay.com/photo/2020/06/29/10/55/pizza-5352320__480.png"
        filename = restaurant["name"] + "_thum"

        qry = f"insert into restaurant_photo (restaurant_id, path, filename) values ('{rId}', '{path}', '{filename}')"
        curs.execute(qry)


def updateDB():
    # DB 연결
    conn = pymysql.connect(host='recoderdbinstance.crnm0s8emitk.ap-northeast-2.rds.amazonaws.com',
                           user='recoder', password='shdudtka123', db='sprint1', charset='utf8')
    curs = conn.cursor()

    f = open('../../filename/filename', 'r')
    names = f.read().split()
    f.close()

    # insertIntoCategory(curs)
    # 넣을 동 개수 조절용
    count = 0
    for filename in names:
        fpath = "../../restaurant_json/" + filename
        jsonData = utils.readJsonFile(fpath)

        try:
            print(filename, " insert 시작")
            # Update Restaurant table
            insertIntoRestaurant(curs, jsonData)
            insertIntoRestaurantCategory(curs, jsonData)
            insertIntoRestaurantPhoto(curs, jsonData)

            print(filename, " insert 완료")
            count += 1
            if count >= 10:
                break
        except Exception as e:
            print(e)
            continue

    # DB닫기
    conn.commit()
