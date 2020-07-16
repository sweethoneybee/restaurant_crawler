import pymysql
import requests


def insertIntoDatabase(results):

    conn = pymysql.connect(host='recoderdbinstance.crnm0s8emitk.ap-northeast-2.rds.amazonaws.com',
                           user='recoder', password='shdudtka123', db='recoderdb', charset='utf8')
    curs = conn.cursor()

    for restaurant in results:
        googleId = restaurant["googleId"]
        naverId = restaurant["naverId"]
        name = restaurant["name"]
        naverReviewCount = restaurant["reviewCount"]
        openTime = restaurant["opentime"]
        status = "영업중" if restaurant["openNow"]["open_now"] else "영업안함"
        phone = restaurant["tel"]
        longitude = restaurant["geometry"]["lng"]
        latitude = restaurant["geometry"]["lat"]
        address = restaurant["address"]
        google_rating = restaurant["googleRating"]
        price = restaurant["priceLevel"] if restaurant["priceLevel"] else -1

        sql = f'insert into restaurant (google_id,naver_id,name,naver_review_count,open_time,status,phone,longitude,latitude,address,google_rating,price) values ("{googleId}",{naverId},"{name}",{naverReviewCount},"{openTime}","{status}","{phone}",{longitude},{latitude},"{address}",{google_rating},{price})'

        curs.execute(sql)
        conn.commit()
