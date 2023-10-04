#!/usr/bin/env python
# coding: utf-8

# In[5]:


from selenium import webdriver
import time


# In[6]:

from selenium.webdriver.chrome.options import Options
import subprocess
import shutil

# 자신 맞는 chrome.exe 위치 변경 필요
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


# In[7]:


# open chrome browser
browser = webdriver.Chrome(executable_path='../chromedriver.exe', options=options)


# In[8]:


# url in address window(주소창에 url 입력)
browser.get('https://www.coupang.com/np/search?q=%EA%B0%84%20%EA%B8%B0%EB%8A%A5%20%EC%98%81%EC%96%91%EC%A0%9C&channel=auto')
browser.implicitly_wait(10)


# ## 상품 사이트 열리지 않음. 클릭해도 열리지 않고, for문으로도 열리지 않음

# In[42]:


import pandas as pd
import pymongo as mg


# In[9]:


click_product ='.search-product-wrap'
product_list = browser.find_elements_by_css_selector(click_product)
len(product_list) # 한 페이지당 36개 상품


# In[ ]:

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = mg.MongoClient(host='mongodb://localhost:27017')
database = client['project_nutrients']
collection = database['coupang_liver_review']

column_name = ['product_name', 'review_date', 'review_content', 'review_star', 'review_writer']


i=3  
h=3
review_list = []
main_window = browser.current_window_handle  # 현재 창의 핸들 저장
from selenium.webdriver.common.keys import Keys
for product in product_list:
    product.click()

    browser.implicitly_wait(10)
    print(f"현재 탭 제목: {browser.title}")   
    time.sleep(2)

    # 새로운 탭이 열릴 때까지 대기 (예시: 2개 이상의 창이 열리고, 그 중 하나가 현재 탬과 다른 창일 때까지 대기)
    wait = WebDriverWait(browser, 10)
    new_tab_handle = wait.until(EC.new_window_is_opened)

    # 모든 탬의 핸들 가져오기
    all_tab_handles = browser.window_handles

    # 새로운 탬의 핸들 찾아 선택하기
    for handle in all_tab_handles:
        if handle != main_window:
            new_tab_handle = handle

    # 새로운 탬으로 전환하기
    browser.switch_to.window(new_tab_handle)

    # 필요한 작업 수행 및 정보 가져오기 (예시: 페이지 제목 가져오기)
    print(f"새로운 탭 제목: {browser.title}")   

    try :
        # 상품평 클릭
        browser.find_element_by_css_selector('#prod-review-nav-link').send_keys(Keys.ENTER)
        page = browser.find_element_by_css_selector('.product-tab-review-count').text
        page = page.replace(",", "")  # 쉼표 제거
        page = page.replace("(", "")  # 왼쪽 괄호 제거
        page = page.replace(")", "")  # 오른쪽 괄호 제거

        # 이제 정수로 변환 시도
        try:
            page_int = int(page)
            print(page_int)
        except ValueError as e:
            print("타입 변환 오류:", e)


        for go in range(1, page_int,1):
            element_path = 'div.sdp-review__article__page.js_reviewArticlePagingContainer > button:nth-child({})'.format(h)
            pagination = browser.find_element_by_css_selector(element_path)
            try:
                product = browser.find_element_by_css_selector(' article:nth-child({}) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info__name'.format(i)).text
                star = browser.find_element_by_css_selector('article:nth-child({}) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info > div.sdp-review__article__list__info__product-info__star-gray > div'.format(i)).get_attribute('data-rating')
                date = browser.find_element_by_css_selector('article:nth-child({}) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info > div.sdp-review__article__list__info__product-info__reg-date'.format(i)).text
                content = browser.find_element_by_css_selector('article:nth-child({}) > div.sdp-review__article__list__review.js_reviewArticleContentContainer > div'.format(i)).text
                writer = browser.find_element_by_css_selector('article:nth-child({}) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__user > span'.format(i)).text
                review_list= [product, date, content, star, writer]
                review_lists.append(review_list)

                print(star)
                i = i + 1        
                if i == 8 :
                    pagination.click()
                    time.sleep(1)
                    h = h + 1
                    i = 3

                if h == 13:  # h 값이 12일 때 다시 3으로 초기화
                    h = 3

                # 저장을 위한 작업 
                df_coupang_liver = pd.DataFrame(data=review_lists, columns=column_name)
                data_dict = df_coupang_liver.to_dict(orient='records')
                collection.insert_many(data_dict)


            except:
                print('실패: {}'.format(element_path))
                break

    except :
        pass

    time.sleep(20)
    # 다시 메인 창으로 전환
    browser.switch_to.window(main_window)
    time.sleep(2)




product_list[0].click()


# In[13]:


#browser.find_element_by_css_selector('#btfTab > ul.tab-titles > li:nth-child(2)')


# In[ ]:


#browser.quitit()