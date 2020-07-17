import requests
import json
import time
import random
import utils


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


def naver_crawling(query, fileName, sleepStart, sleepEnd):
    rId = 1
    array = []
    for page in range(1, 4):
        URL = f"https://map.naver.com/v5/api/search?caller=pcweb&query={query}&type=all&page={page}&displayCount=100&isPlaceRecommendationReplace=true&lang=ko"
        response = requests.get(URL).json()["result"]["place"]["list"]
        for restaurant in response:
            tmp = {}
            tmp["rId"] = rId
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
            rId += 1
        with open(f"../../restaurant_json/{fileName}.json", "w") as json_file:
            json.dump(array, json_file, ensure_ascii=False)

        print(f"({page} / 3)page 긁기 성공!")
        utils.logging(f"({page} / 3)page 긁기 성공!")
        if page < 3:
            #    sleepTime = random.randint(sleepStart, sleepEnd)
            sleepTime = 5
            print("다음 페이지 긁기 전", sleepTime, "초 기다리는 중...")
            utils.logging("다음 페이지 긁기 전", str(sleepTime), "초 기다리는 중...")
            time.sleep(sleepTime)
        else:
            print("======== \'", query, "\' 긁기 완료 ========")
            utils.logging("======== \'", query, "\' 긁기 완료 ========")
            return rId-1
        # if page >= 3:
        #     print("======== \'", query, "\' 긁기 완료 ========")
        #     utils.logging("======== \'", query, "\' 긁기 완료 ========")
        #     return rId - 1


def naver_crawling_with_dong():
    numberOfRestaurant = 0
    with open("../../dong_json/seoul_dong.json", "r") as json_file:
        json_data = json.load(json_file)
        temp = 0
        print("\n", time.strftime('%c', time.localtime(time.time())), "크롤링 시작!")
        utils.logging(time.strftime(
            '%c', time.localtime(time.time())), "크롤링 시작!")
        # for dong in json_data:
        # 나눠서 긁어오기 위해 range의 값을 시작값을 조정해주면서 함.
        # 현재 199까지 긁음.
        # 새로 시작한 것 56까지 긁음
        indexNum = utils.readCrawlIndex()
        for i in range(indexNum, len(json_data)):
            dong = json_data[i]
            dongName = dong["DONG"]
            query = dongName + " 식당"

            fileName = dong["JACHIGU"] + "_" + dong["DONG"]
            print("======== \'", query, "\'의 json을 긁어오기 시작함 ========")
            utils.logging("======== \'", query,
                          "\'의 json을 긁어오기 시작함 ========")
            numberOfRestaurant += naver_crawling(query, fileName, 3, 10)

            temp += 1
            print(i, "번째 동 긁어오기 성공")
            utils.logging(str(i), "번째 동 긁어오기 성공")
            utils.saveFilename(fileName)
            utils.saveCrawlIndex(i)

            if temp >= 30:
                print()
                utils.logging("")
                print("총", numberOfRestaurant, "개의 식당을 찾았습니다.")
                utils.logging("총", str(numberOfRestaurant), "개의 식당을 찾았습니다.")
                print(i, "인덱스까지 긁음")
                utils.logging(str(i), "인덱스까지 긁음")

                print(time.strftime('%c', time.localtime(time.time())),
                      "다음 크롤링 싸이클을 위해 60분 대기 중...")
                utils.logging(time.strftime('%c', time.localtime(
                    time.time())), "다음 크롤링 싸이클을 위해 60분 대기 중...")
                time.sleep(60 * 60)

                # 재시작전 변수 초기화
                temp = 0
                numberOfRestaurant = 0
                print(time.strftime('%c', time.localtime(time.time())), "크롤링 재시작!")
                utils.logging(time.strftime(
                    '%c', time.localtime(time.time())), "크롤링 재시작!")
                continue

            # termTime = random.randint(11, 23)
            termTime = 45
            print("다음 동을 긁기 전", termTime, "초 기다리는 중...")
            utils.logging("다음 동을 긁기 전", str(termTime), "초 기다리는 중...")
            time.sleep(termTime)
