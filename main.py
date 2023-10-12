# conda install -c conda-forge fastapi uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# No 'Access-Control-Allow-Origin'
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 접근 가능한 도메인만 허용하는 것이 좋습니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

import pickle

# /api_v1/mlmodelwithregression with dict params
# method : post

@app.post('/api_v1/mlmodelwithregression') 
def mlmodelwithregression(data:dict) : 
    print('data with dict {}'.format(data))
    # data dict to 변수 활당
    review_content = data['review_content'] ## str로 입력되면 변환 안해도 될듯?
    # 입원기간 = float(data['입원기간'])
    # 통증기간 = float(data['통증기간(월)'])

## 전처리 pkl 불러오기
 # 전처리 형태소 분석 pkl
    with open('gatheringdatas/datasets/tokenized_reviews.pkl', 'rb') as preprocess_token: 
        token_loaded_scaler = pickle.load(preprocess_token)
        token_input_scaler = ['review_content']
        token_input_features = token_loaded_scaler.transform([review_content])
        
        ### input : reveiw_content ⇒ output : tokenized_reviews

 # 전처리 불용어처리 pkl
    with open('gatheringdatas/datasets/replaced_review.pkl', 'rb') as preprocess_stopword: 
        replaced_loaded_scaler = pickle.load(preprocess_stopword)
        replaced_input_scaler = ['tokenized_reviews']
        replaced_input_features = replaced_loaded_scaler.transform(token_input_features)
        #### input : tokenized_reviews ⇒ output : replaced_review


## machinelearning _ 진행 column['replaced_review']
 # 전처리 _ tfidfVectorization
    with open('gatheringdatas/datasets/tfidfVectorizer.pkl', 'rb') as tvector: 
        loaded_scaler = pickle.load(tvector)
        input_scaler = ['replaced_review']
        input_features = loaded_scaler.transform(replaced_input_features)


    result_predict = 0;
 # final _ SVC 예측 
    with open('gatheringdatas/datasets/sentiment_analyze_mechinelearning.pkl', 'rb') as predict_SVC: 
        loaded_model = pickle.load(predict_SVC)
        result_predict = loaded_model.predict(input_features)
        
        print('review reponse : {}'.format(result_predict))
        pass
    

        # # 예측값 리턴
        # result = int({'Location_of_herniation':result_predict[0]})
        # return result
        result = {'review reponse' : result_predict}
        return result



