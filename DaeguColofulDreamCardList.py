from selenium import webdriver

CHROME_DRIVER_PATH  = 'D:/05. workspace/02. Python/cli/MealServiceWebCrawlerProject/chromedriver.exe'
URL                 = 'http://www.colorfulcard.or.kr/franchise/search'
driver              = webdriver.Chrome(CHROME_DRIVER_PATH)


def getPageTableRowData(driver):
    mobileScroll = driver.find_element_by_class_name("mobile-scroll")
    tableRowList = mobileScroll.find_elements_by_tag_name("tr")
    for rowIdx in tableRowList:
        print(rowIdx.text.encode('utf-8') + ',')


def navigatePagination(driver):
    pagination = driver.find_element_by_class_name("pagination")
    ulItem = pagination.find_element_by_tag_name("ul")
    pageList = ulItem.find_elements_by_tag_name("a")

    for pageIdx in pageList:
        print(pageIdx.text.encode('utf-8'))  # encode exception handling


def clickNextPage(driver):
    pagination = driver.find_element_by_class_name("pagination")
    ulItem = pagination.find_element_by_tag_name("ul")
    pageList = ulItem.find_elements_by_tag_name("a")
    for pageIdx in pageList:
        if(pageIdx.text.encode('utf-8') == '2'):
            pageIdx.click().perform()
            break




driver.implicitly_wait(3)
driver.get(URL)
getPageTableRowData(driver)
navigatePagination(driver)
clickNextPage(driver)



