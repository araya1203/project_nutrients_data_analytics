#!/usr/bin/env python
# coding: utf-8

# ## project_nutrients_review_positive

# In[1]:


import pandas as pd
df_review_positive = pd.read_csv('gatheringdatas/datasets/reviews_data/final_all_preprocess_positive.csv')


# In[2]:


df_review_positive.info()


# In[3]:


df_review_positive = df_review_positive.dropna()


# ### LDA 분석

# ##### 문장 벡터화

# In[4]:


from gensim.corpora import Dictionary
from gensim.models import LdaModel


# In[5]:


# 'replaced_review' 열의 모든 값을 문자열로 변환
df_review_positive['replaced_review'] = df_review_positive['replaced_review'].astype(str)


# In[6]:


dictionary = Dictionary(df_review_positive[['replaced_review']].values)
dictionary


# In[7]:


# dictionary에 의한 한글 문장을 벡터화 변환
corpus_list = list()
for sentence in df_review_positive[['replaced_review']].values :
  vectors = dictionary.doc2bow(sentence)
  corpus_list.append(vectors)


# In[8]:


df_review_positive['문장벡터화'] = corpus_list


# In[9]:


df_review_positive[:3]


# ##### 토픽 잡기(review_positive)
# - review_positive.csv 토픽 분석
# - 토픽 수 9 <<<<<<< 변경하기 

# In[10]:


lda_model = LdaModel(corpus=corpus_list, id2word=dictionary, num_topics=9)


# In[11]:


lda_model.print_topics(num_words=4)


# ##### 최적에 토픽 단어 수

# In[12]:


sentences = df_review_positive['replaced_review']
sentences


# In[13]:


type(sentences)


# In[14]:


# 각 문장을 공백으로 나누어 리스트에 저장
tokenized_sentences = [sentence.split() for sentence in sentences]


# In[15]:


# 결과 출력
morphs_list = list()
for tokens in tokenized_sentences:
    morphs_list.append(tokens)
morphs_list


# In[16]:


preprocessed_sentences = morphs_list


# In[17]:


dictionary_dic = Dictionary(preprocessed_sentences) # fix in like sklean
dictionary_dic


# In[18]:


# 데이터 프레임에서 열 데이터 확인
print(df_review_positive[['replaced_review']].head())


# In[19]:


# morphs_list 확인
print(morphs_list[:5])  # 처음 몇 개의 항목 출력


# In[22]:


# dictionary 객체 확인 (일부 단어만 출력)
print(list(dictionary_dic.token2id.items())[:10])


# In[23]:


# 일관성 점수
from gensim.models.coherencemodel import CoherenceModel
coherenceModel = CoherenceModel(model=lda_model, texts=morphs_list, dictionary=dictionary_dic)
coherenceModel.get_coherence()


# In[20]:


# 혼잡도 점수
lda_model.log_perplexity(corpus_list)


# In[21]:


lda_model.num_topics


# In[ ]:





# In[22]:


start_topic = 10
end_topic = 20
coherence_scores = list()
perplexity_scores = list()
for topic_number in range(start_topic, end_topic+1):
    best_lda_model = LdaModel(corpus=corpus_list, id2word=dictionary, num_topics=topic_number) # fix
    coherenceModel = CoherenceModel(model=best_lda_model, texts=morphs_list, dictionary=dictionary)
    coherence_scores.append(coherenceModel.get_coherence()) # 일관성 점수
    perplexity_scores.append(best_lda_model.log_perplexity(corpus_list))


# In[ ]:


import pandas as pd
scores = pd.DataFrame([coherence_scores,  perplexity_scores]).T
scores


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


sns.lineplot(coherence_scores)
plt.show()
sns.lineplot(perplexity_scores)
plt.show()


# ##### LDA 시각화

# In[ ]:


pyLDAvis.enable_notebook() # 일반적인 python에선 불필요
result_visualized = pyLDAvis.gensim_models.prepare(lda_model, corpus_list, dictionary)


# In[ ]:


pyLDAvis.display(result_visualized)


# In[ ]:


pyLDAvis.save_html(result_visualized, '../project_nutrients_review_positive_result_visualized.html')

