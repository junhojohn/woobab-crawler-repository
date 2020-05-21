# -*- coding: utf-8 -*-

# 2020.05.20 junhojohn.
# https://www.purmeecard.com/public/merchantSelectForm2.jsp?request=merchantSelectForm 에 접속하여
# 모든 가맹점 정보를 웹 크롤링하여 txt파일로 떨구는 프로그램이다.

# import 라이브러리
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cStringIO import StringIO
import time

#필드1: chromedriver.exe파일경로
CHROME_DRIVER_PATH          = 'D:/05. workspace/02. Python/cli/MealServiceWebCrawlerProject01/chromedriver.exe'
#필드2: 접근할 URL
URL                         = 'https://www.purmeecard.com/public/merchantSelectForm2.jsp?request=merchantSelectForm'
# 필드3: chromedriver.exe실행하여 얻은 Proxy 웹 브라우저 객체
driver                      = webdriver.Chrome(CHROME_DRIVER_PATH)
# 필드4: active한 페이지인지 페이지를 순회하며 찾을 때 순회를 시작할 인덱스
currentPageNum = 1
# 문자열 Append를 위한 StringIO객체
file_str = StringIO()
# 필드5: 텍스트파일 출력경로
OUTPUT_PATH                 = 'D:/05. workspace/02. Python/cli/output/Pureumi-card.txt'
# 필드6: 페이지 안 테이블 컬럼 수(구분, 가맹점명, 전화번호, 주소, 가맹구분)
dataColumnCnt               = 7
# 필드7: 다음 10개 보기할 때 아이콘에 표시되는 문자열
paginationStr               = "https://www.purmeecard.com/images/nxt.gif"


def clickAllProvince(driver):
    # <iframe> 태그 다음에 #document에 접근한다.
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    # 지역 콤보박스에서 -----전체를 선택한다.
    selectItem = driver.find_element_by_tag_name("select")
    optionList = selectItem.find_elements_by_tag_name("option")
    optionList[0].click()

def getTableRowData():
    cellList = driver.find_elements_by_xpath('/html/body/table/tbody/tr[4]/td/div/table/tbody/tr/td')

    cnt = 0
    for cellIdx in range(6, len(cellList)):
        if(cnt == dataColumnCnt):
            cnt = 0
            file_str.write('\n')

        if(cellList[cellIdx].text.encode('utf-8') is not None):
            file_str.write(cellList[cellIdx].text.encode('utf-8'))
        else:
            file_str.write(' ')
        file_str.write(',')
        cnt+=1
        

def clickNextPage(driver, currentPageNum):
    pageItem = driver.find_element_by_class_name("paging")
    pageList = pageItem.find_elements_by_tag_name("a")

    getTableRowData()

    if(currentPageNum%10 != 0):
        currentPageNum+=1
        for pageItem in pageList:
            if(pageItem.text.encode('utf-8') == str(currentPageNum)):
                pageItem.click()
                break
        return currentPageNum

    else:
        currentPageNum += 1
        imgTagList = pageItem.find_elements_by_tag_name("img")
        for imgItem in imgTagList:
            if(imgItem.get_attribute("src") == paginationStr):
                imgItem.click()
                break
        return currentPageNum


# 함수3: 가맹점 검색결과를 텍스트 파일로 내보낸다.
def createStoreSearchResultFile():
    text = open(OUTPUT_PATH, 'w')
    text.write(file_str.getvalue())
    text.close()


# 메인로직1: Chrome 프록시를 띄우고 URL에 접속한다.
driver.get(URL)
# 메인로직2: 페이지가 로드될 때까지 3초 기다린다.
driver.implicitly_wait(3000)
# 메인로직3: 전체 지방을 선택한다.
clickAllProvince(driver)

while currentPageNum < 64:
    currentPageNum = clickNextPage(driver, currentPageNum)
# 메인로직5: 크롤링한 모든 가맹점 정보를 텍스트 파일로 출력
createStoreSearchResultFile()
# 메인로직6: 모든 페이지를 방문하고 나면 Chrome Proxy 웹 브라우저 객체 자원을 닫기 및 반환한다.
driver.close()
driver.quit()