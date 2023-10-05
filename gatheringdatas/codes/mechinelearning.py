#!/usr/bin/env python
# coding: utf-8

# ### 벡터 토큰화(단어 숫자화)

# In[1]:


import pandas as pd
df_review_positive = pd.read_csv('gatheringdatas/datasets/reviews_data/all_preprocess_positive.csv')
df_review_negative = pd.read_csv('gatheringdatas/datasets/reviews_data/all_preprocess_negative.csv') 


# In[2]:


len(df_review_positive)


# In[3]:


len(df_review_negative)


# In[4]:


condition_positive = df_review_positive['review_star'] == 5 # postive_reviews 89917 negative_reviews 709로 확인되어 postive_reviews 중 review_star 5인 것으로 postive_reviews 사용하기로 함. 


# In[5]:


df_review_positive = df_review_positive[condition_positive]


# In[6]:


df_review_positive # review_star 5갯수는 65426 rows


# In[7]:


condition_negative = df_review_negative['review_star'] <= 3 


# In[8]:


df_review_negative = df_review_negative[condition_negative]


# In[9]:


df_review_negative # negative_reviews 4821 


# In[10]:


comments_positive = df_review_positive['replaced_review'].tolist()
comments_positive


# In[ ]:





# In[11]:


comments_negative = df_review_negative['replaced_review'].tolist()
comments_negative


# In[12]:


len(comments_positive), len(comments_negative)


# In[13]:


comments_positive = comments_positive[0:4821]


# In[14]:


comments_positive


# In[15]:


comments_list = comments_positive + comments_negative


# In[16]:


comments_list


# ### 형태소 분석기 통한 품사 분류

# In[17]:


from mecab import MeCab
mecab = MeCab()


# In[18]:


mecab.pos(comments_list[0])


# In[ ]:


tokenized_comments = list()
for comment in comments_list:
    try:
        comment_morphs = mecab.morphs(comment)
        # 추가로 불용어 처리 필요
        tokenized_comments.append(comment_morphs)
    except Exception as e:
        # 예외가 발생했을 때 처리할 코드를 여기에 추가합니다.
        print(f"An error occurred: {str(e)}")
        # 예외 발생 시 현재 comment를 건너뛰고 다음 comment로 진행합니다.
        continue
print(tokenized_comments)

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


# In[ ]:


comments = list()
for token in tokenized_comments:
    comments.append(' '.join(token))
# 리스트 안의 리스트를 한 문장으로 결합


# In[34]:


comments 


# In[27]:


countVectorizer = CountVectorizer()
countVectorizer.fit(comments)


# In[ ]:


countVectorizer.vocabulary_


# In[ ]:


tfidfVectorizer = TfidfVectorizer(use_idf=True)
tfidfVectorizer.fit(comments)


# In[ ]:


tfidfVectorizer.idf_


# In[ ]:


feature = tfidfVectorizer.transform([comments[9]]) # 학습 시 2차원을 이용했으므로 변환도 2차원 적용
feature.toarray() # vocabulary_ 갯수와 사이즈가 같음.


# In[ ]:


features = tfidfVectorizer.transform(comments) # 댓글 전체 벡터화


# ### 목표 변수 생성

# In[ ]:


target = ['긍정'] * len(comments_positive)  + ['부정'] * len(comments_negative)
# target


# ### 머신러닝 학습

# In[ ]:


from sklearn.svm import SVC


# In[ ]:


model = SVC()
model.fit(features.toarray(), target)


# ### 머신러닝 통한 예측

# In[ ]:




