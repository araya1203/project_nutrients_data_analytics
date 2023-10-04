#!/usr/bin/env python
# coding: utf-8

# In[1]:
## 피로영양제, 많은 리뷰순으로 가져옴


from selenium import webdriver
import time
import pandas as pd


# In[2]:


import pymongo as mg
client = mg.MongoClient(host='mongodb://localhost:27017')
database = client['project_nutrients']
collection = database['recovery_elevenstreet_review']


# In[3]:


from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options
import subprocess
import shutil


# In[4]:


subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


# In[5]:


#open chrome browser
browser = webdriver.Chrome(executable_path='C:/Users/01-15/Develops/chromedriver.exe', options=options) #webdriver_selenium과 web을 연결해주기위함.
browser.set_window_size(1560,2000)


# In[6]:


# url in address window
## final 피로 영양제 
browser.get('https://search.11st.co.kr/pc/total-search?kwd=%25ED%2594%25BC%25EB%25A1%259C%2520%25EC%2598%2581%25EC%2596%2591%25EC%25A0%259C&tabId=TOTAL_SEARCH')
browser.implicitly_wait(10)


# In[7]:


## 리뷰 많은 순 클릭
click_path='#layBodyWrap > div > div > div.l_search_content > div.search_content > div.c_search_sorting > div > div > div > div'
browser.find_element_by_css_selector(click_path).click()
time.sleep(2)
select_category='div.c_search_sorting > div > div > div > ul > li:nth-child(5)'
browser.find_element_by_css_selector(select_category).click()


# In[8]:


## pagination 하기
# 검색 결과 # div.search_content > div > p > span
product_total = browser.find_element_by_css_selector('div.search_content > div > p > span')
product_total_str = product_total.text
# 쉼표를 제거합니다.
product_total_del = product_total_str.replace(',', '')
product_total_count = int(product_total_del)


# In[9]:


print(product_total_count) ## 검색 결과_숫자

product_standard_count_per = 60 ## 상품목록수


# In[10]:


loop_count_int = int(product_total_count / product_standard_count_per) 
print(loop_count_int) ## 상품 총 페이지수 


# 현재 페이지 번호를 초기화합니다.
current_page = 1
# pagination 버튼을 끝까지 순환하면서 페이지 이동합니다.
while current_page <= loop_count_int:
    try:
        
        for i in range(1, 61):  # 1부터 60까지 순회합니다.
            try:
                time.sleep(5)
                product_page = f'#section_commonPrd > div.c-search-list > ul > li:nth-child({i}) > div > a'
                product = browser.find_element_by_css_selector(product_page)
                product.click()
                # 새로 열린 창으로 브라우저 컨텍스트를 전환합니다.
                browser.switch_to.window(browser.window_handles[-1]) 
                time.sleep(5)
                ## -> browser.window_handles[-]하면 옆으로 쭉쭉 생기는건가봄. 
                ## 여기부터 리뷰 더보기 클릭하기 
                product_name= browser.find_element_by_css_selector('div.c_product_info_title > h1').text
                print(product_name)
                # 리뷰보기 클릭 불필요
                browser.switch_to.frame('ifrmReview')
                click_count = 0
                while True:
                    try:
                        # 리뷰 더보기 버튼을 찾습니다.
                        
                        button = '#review-list-page-area > div > button'
                        button_click=browser.find_element_by_css_selector(button)
                        
                        # 리뷰 더보기 버튼을 클릭합니다.
                        button_click.click()
                        
                        # click_count += 1  # 클릭 횟수 증가
        
                        # 만약 클릭 횟수가 15번 이상이면 반복 종료
                        # if click_count >= 20:
                        #     break
                    except:
                        # 리뷰 더보기 버튼을 더 이상 찾을 수 없으면 반복 종료합니다.
                        print('리뷰 더보기 버튼을 더 이상 찾을 수 없음')
                         # 클릭 후 잠시 대기합니다 (사이트 로딩에 따라 조절)
                        break
                ## 일단 총 리뷰수를 int로 바꾼다. 
                review_total_count_text = browser.find_element_by_css_selector('h4 > span > i').text
                    
                ## 혜인설명: 총 댓글 수를 정규화로 뽑아냄 .
                # 정규 표현식을 사용하여 숫자 추출 (',' 포함)
                import re
                result_list = re.findall(r'\d+', review_total_count_text)

                # 추출된 숫자들을 하나의 문자열로 결합하고 ',' 제거
                review_count = ''.join(result_list)

                # 문자열을 정수로 변환
                review_total_count = int(review_count)  # 리뷰 총 갯수 
                print(review_total_count)
                time.sleep(3)
                # 리뷰 50개 이상이면 돌린다. 
                if review_total_count != 0:
                    ##리뷰 번들
                    reviews_bundle = browser.find_elements_by_css_selector('.review_list_element')
                    len(reviews_bundle)
                    ## 리뷰 리스트
                    eyes_product_columns_name = ['product_name','review_content', 'review_date', 'review_star', 'review_writer']
                    reviews_list = list()

                    for number in reviews_bundle:
                            try:
                                try:  
                                    review_content = number.find_element_by_css_selector('div.c_product_review_cont > div').text ##bundle에서 0번째 가져옴?
                                    # review_content = re.sub(r'<br\s*/*>|\\n', ' ', review_text)
                                except: 
                                    review_content = str()
                                try:  
                                    review_date = number.find_element_by_css_selector('div.c_product_review_cont > p.side > span').text 
                                except: 
                                    review_date = str()
                                try:  
                                    review_star = number.find_element_by_css_selector('p.grade > span > em').text
                                except: 
                                    review_star = str()
                                try:  
                                    review_writer = number.find_element_by_css_selector('dl > dt').text 
                                except: 
                                    review_writer = str()
                                
                                # 리뷰 정보를 리스트로 저장하고 리스트에 추가
                                
                                review_data = [product_name, review_content, review_date, review_star, review_writer]
                                # print(review_data)
                                reviews_list.append(review_data)

                            except:
                                print('리뷰완료')
                                pass  # Break out of the loop if the lengths match
                    
                    df_reviews = pd.DataFrame(data=reviews_list, columns=eyes_product_columns_name)
                    data_dict = df_reviews.to_dict(orient='records')
                    collection.insert_many(data_dict)
                    
                    print(len(reviews_list))
                    # Check again after the inner loop to break from the outer loop
                    if len(reviews_list) == len(reviews_bundle):
                        print('상품리뷰완료')
                    
                else :
                    if review_total_count < 21:
                        print('리뷰가 적어서 종료합니다.') # 리뷰 50이하면 종료
                    break

                # 현재 페이지를 닫습니다.
                browser.close()
                # 다음 상품을 클릭하기 전에 원래의 창으로 다시 전환합니다.
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(5)          
            except:
                    break
        if review_total_count < 21:
            break  # 외부 루프 종료

        if current_page > loop_count_int:
            print('더 이상 페이지가 없어 종료합니다.')
            break  # 루프 종료        
        current_page += 1
        page_button_css = f'#section_commonPrd > nav > ul > li:nth-child({current_page % 10 + 2}) > button'
        page_button = browser.find_element_by_css_selector(page_button_css)
        page_button.click()
    except:        
        print('더이상 리뷰가 존재하지 않아 종료')
        break
    

