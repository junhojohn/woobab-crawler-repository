# -*- coding: utf-8 -*-

# 2020.05.20 junhojohn.
# http://www.colorfulcard.or.kr/franchise/search 에 접속하여
# 모든 가맹점 정보를 웹 크롤링하여 txt파일로 떨구는 프로그램이다.

# import 라이브러리
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cStringIO import StringIO

#필드1: chromedriver.exe파일경로
CHROME_DRIVER_PATH          = 'D:/05. workspace/02. Python/cli/MealServiceWebCrawlerProject01/chromedriver.exe'
#필드2: 접근할 URL
URL                         = 'http://www.colorfulcard.or.kr/franchise/search'
# 필드3: chromedriver.exe실행하여 얻은 Proxy 웹 브라우저 객체
driver                      = webdriver.Chrome(CHROME_DRIVER_PATH)
# 필드4: active한 페이지인지 페이지를 순회하며 찾을 때 순회를 시작할 인덱스
startFindingActivePageIdx   = 0
# 문자열 Append를 위한 StringIO객체
file_str = StringIO()
# 필드5: 텍스트파일 출력경로
OUTPUT_PATH                 = 'D:/05. workspace/02. Python/cli/output/Daegu_colorful.txt'
# 필드6: 페이지 안 테이블 컬럼 수(구분, 가맹점명, 전화번호, 주소, 가맹구분)
dataColumnCnt               = 5
# 필드7: 다음 10개 보기할 때 아이콘에 표시되는 문자열
paginationStr               = '»'


#함수1: 현재 active된 페이지의 테이블 행 정보들을 모두 가져온다. 인자1: ChromeWebDriver
def getPageTableRowData(driver):
    mobileScroll = driver.find_element_by_class_name("mobile-scroll")
    cellList = mobileScroll.find_elements_by_tag_name("td")
    cnt = 0
    for cellIdx in cellList:
        if(cnt == dataColumnCnt):
            cnt = 0
            file_str.write('\n')

        file_str.write(cellIdx.text.encode('utf-8'))
        file_str.write(',')
        cnt+=1


#함수2: 현재 active된 페이지의 다음 페이지 번호를 클릭한다. 인자1: ChromeWebDriver, 인자2: active한 페이지인지 페이지를 순회하며 찾을 때 순회를 시작할 인덱스
def clickNextPage(driver, startFindingActivePageIdx):

    pagination = driver.find_element_by_class_name("pagination")
    ulItem = pagination.find_element_by_tag_name("ul")
    pageList = ulItem.find_elements_by_tag_name("a")

    for pageIdx in range(startFindingActivePageIdx, len(pageList)):
        pageItem = pageList[pageIdx]
        classAttr = pageItem.get_attribute("class")
        if(classAttr == 'active'):
            getPageTableRowData(driver)
        else:
            pageNumStrVal = pageItem.text.encode('utf-8')
            pageItem.click()
            if(pageNumStrVal == paginationStr):
                return 1
            else:
                return pageIdx

# 함수3: 가맹점 검색결과를 텍스트 파일로 내보낸다.
def createStoreSearchResultFile():
    text = open(OUTPUT_PATH, 'w')
    text.write(file_str.getvalue())
    text.close()

# 메인로직1: Chrome 프록시를 띄우고 URL에 접속한다.
driver.get(URL)
# 메인로직2: 페이지가 로드될 때까지 3초 기다린다.
driver.implicitly_wait(3000)
# 메인로직3: 모든 페이지를 순회하면서 (<a href=""... class="active"> 가 없을 때까지 while루프를 돌면서)
while startFindingActivePageIdx is not None:
    # 클릭 이벤트를 자동으로 발생시킨다.
    startFindingActivePageIdx = clickNextPage(driver,  startFindingActivePageIdx)
    # 클릭을 함으로써 페이지의 DOM객체들을 페이지에 로드하는 시간을 기다려 주어야 한다. <a> 태그가 모두 로드될 때까지 기다린다. 넉넉히 최대 3초까지 기다린다.
    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
# 메인로직4: 크롤링한 모든 가맹점 정보를 텍스트 파일로 출력
createStoreSearchResultFile()
# 메인로직5: 모든 페이지를 방문하고 나면 Chrome Proxy 웹 브라우저 객체 자원을 닫기 및 반환한다.
driver.close()
driver.quit()