## 🐾 프로젝트 설명

- 영양제 추천 홈페이지를 위해 11번가와 쿠팡의 기능별 영양제 리뷰 데이터를 수집하고, 별점을 기준으로 긍정과 부정으로 나눕니다.
  이후 데이터를 분석하여 긍정/부정 댓글을 판단하는 머신러닝 모델을 훈련하고, 긍정 댓글이 많은 영양제를 추천 리스트로 제공합니다.
  이 프로젝트는 영양제 선택을 돕는 서비스를 구현하는데 중점을 두고 있습니다.

<details>
<summary> 데이터 분석 과정 </summary>
  
### 💊 리뷰 수집  
     11번가와 쿠팡에서 각 기능별 영양제 검색, 상품별 리뷰를 수집
     * 쿠팡은 상품당 50개의 리뷰만 수집이 됨.

### 💊 데이터 전처리 
     수집한 데이터를 정제하고 필요한 정보를 추출.
     별점을 기준으로 3점이하는 부정, 3점 초과는 긍정으로 데이터를 분리.
     중복된 리뷰나 불요어 제거, 단어를 치환하여 데이터를 정리.
   
### 💊 토픽 모델링: 
     긍정 댓글과 부정 댓글에서 주요 토픽을 추출.
     토픽 모델링 알고리즘을 사용하여 리뷰가 어떤 주제에 관한 것인지 식별.

### 💊 머신러닝 모델 훈련: 
     감정 분석 결과를 기반으로 긍정과 부정을 판단하는 머신러닝 모델을 훈련.
     텍스트 분류 알고리즘을 사용하여 리뷰를 긍정 또는 부정으로 분류.

### 💊 영양제 추천 시스템: 
     긍정적인 리뷰가 많은 영양제를 선정하여 추천 리스트를 생성.
     사용자에게 긍정적인 평가를 받은 영양제를 보여줌으로써 영양제 추천 서비스를 제공.


</details>


## 🐾 LDA 최적의 토픽 및 모델링 결과
* pyLDAvis 패키지를 활용하여 LDA 토픽 모델링 결과 시각화



### ❗ LDA 최적의 토픽 갯수 (일관성 점수 높고, 혼잡도 점수 낮은 토픽)

<div align="center">

![image](https://github.com/araya1203/project_nutrients_data_analytics/assets/132973456/7339dcee-eeeb-475e-8d13-9c544bf49332)






</div>

### ❗ LDA positive 토픽 모델링 결과


<div align="center">
  
![image](https://github.com/araya1203/project_nutrients_data_analytics/assets/132973456/260bd80d-7786-4a7c-90d6-632af857937b)
    
겹치는 토픽이 없는 최적의 토픽 갯수 (3)

</div>    


### ❗ LDA negative 토픽 모델링 결과


<div align="center">
  
![image](https://github.com/araya1203/project_nutrients_data_analytics/assets/132973456/a095dacf-6be3-4816-ab4c-2f788bc462e7)
    
겹치는 토픽이 없는 최적의 토픽 갯수 (4)

</div>



## 🐾 인사이트 도출
<details>
<summary> 콜레스테롤 영양제 긍정적 리뷰 분석</summary>
  
![image](https://github.com/araya1203/project_nutrients_data_analytics/assets/132973456/b8eea9af-410f-43e3-9d43-c9d9f8b43fe0)

</details>


<details>
<summary> 콜레스테롤 영양제 부정적 리뷰 분석</summary>
  
![image](https://github.com/araya1203/project_nutrients_data_analytics/assets/132973456/37a80317-b1a6-444c-94e0-362a637b4ff8)

</details>







