import requests
import json
import time
import utils
import sys


def createMenu(menus):
    if menus == None:
        return []
    splitedMenus = menus.split('|')
    results = []
    for menu in splitedMenus:
        menu = menu.strip()
        item = {}
        for letter in range(len(menu)-1, -1, -1):
            if menu[letter] == " ":
                item["name"] = menu[:letter]
                item["price"] = menu[letter+1:]
                results.append(item)
                break
    return results


def naver_crawling(query, fileName, restaurantId):
    utils.logging("======== \'", query,
                  "\'의 json을 긁어오기 시작함 ========")

    array = []

    page = 0
    while page < 3:
        page += 1
        URL = f"https://map.naver.com/v5/api/search?caller=pcweb&query={query}&type=all&page={page}&displayCount=100&isPlaceRecommendationReplace=true&lang=ko"
        try:
            response = requests.get(URL).json()["result"]["place"]["list"]
        except TimeoutError as te:
            utils.logging("에러 발생:", str(te))
            sys.exit()
        except Exception as e:
            utils.logging(str(e), "때문에 막힘")
            utils.logging(str(page), "막혀서 1분 1초 대기중...")
            time.sleep(61)

            # 다시 시도
            utils.logging(str(page), "페이지 재시도")
            page -= 1
            continue

        for restaurant in response:
            tmp = {}
            tmp["restaurantId"] = restaurantId
            tmp["naverId"] = restaurant["id"]
            tmp["name"] = restaurant["name"]
            tmp["numberOfNaverReviews"] = restaurant["reviewCount"]
            tmp["tel"] = restaurant["tel"]
            tmp["category"] = restaurant["category"]
            tmp["address"] = restaurant["address"]
            tmp["roadAddress"] = restaurant["roadAddress"]
            tmp["thumUrl"] = restaurant["thumUrl"]
            tmp["lat"] = restaurant["y"]
            tmp["lng"] = restaurant["x"]
            tmp["openTime"] = restaurant["bizhourInfo"]
            tmp["menuInfo"] = createMenu(restaurant["menuInfo"])
            array.append(tmp)
            restaurantId += 1

        # 크롤링 결과 저장 경로
        with open(f"./restaurant_화양동/{fileName}.json", "w") as json_file:
            json.dump(array, json_file, ensure_ascii=False)

        utils.logging(f"({page} / 3)page 긁기 성공!")
        if page < 3:
            sleepTime = 5
            utils.logging("다음 페이지 긁기 전", str(sleepTime), "초 기다리는 중...")
            time.sleep(sleepTime)
        else:
            utils.logging("======== \'", query, "\' 긁기 완료 ========")
            return restaurantId-1
        # if page >= 3:
        #     utils.logging("======== \'", query, "\' 긁기 완료 ========")
        #     return restaurantId - 1


def set_crawling_query():
    # PK
    restaurantId = 1

    qrys = ["화양동 맛집", "화양동 저녁", "화양동 한식", "화양동 일식", "화양동 중식",
            "화양동 양식", "화양동 카페", "화양동 치킨", "화양동 족발", "화양동 피자",
            "화양동 분식", "화양동 고기", "화양동 파스타", "화양동 술집"]

    utils.logging("크롤링 시작!")
    for qry in qrys:
        restaurantId = 1

        fileName = qry[:qry.find(" ")] + "_" + qry[qry.find(" ") + 1:]
        restaurantId = naver_crawling(qry, fileName, restaurantId)

        utils.logging(qry, "긁어오기 성공")
        utils.saveFilename(fileName, "./restaurant_화양동/filename")

        termTime = 45
        utils.logging("다음 동을 긁기 전", str(termTime), "초 기다리는 중...")
        time.sleep(termTime)
    utils.logging("쿼리문 = ", str(qrys), "에 대해 요청한 크롤링 완료")


if __name__ == "__main__":
    set_crawling_query()
