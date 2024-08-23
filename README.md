# 클라우드 프로젝트
# #azure funcion, azure storage, python, html, figma
# 일기분석기반 영화추천서비스(azure serverless사용)

- 프로젝트 목적
  - 감정이 우울한 사람들을 위한 영화추천 웹사이트
  - 그날에 맞는 영화추천과 동시에 일기장 기능 수행
  - 감정분석은 유저가 작성한 일기장을 통해서 진행
  - 선택하는 영화에 따라 유저에 대한 성향 파악 후 영화추천이 달라짐

- 구현기능
  - 일기장
  - 회원관리
  - 감정분류
  - 영화추천

---

## 프로그램 구성도 + 데이터 흐름
![img1](https://github.com/user-attachments/assets/eb25f6ba-3550-4615-92e3-69ecc1c8b5ab)

> azure serverless를 사용하려면 함수앱이 필요하고 **모델을 외부에서 따로 만들어 함수앱에서 이용하는 방식** 사용


---

문장을 통하여 감정을 분류하는 모델은 따로 학습하여 사용하도록한다
>cloudproject_Emotion\azure_function_code\감정분류\detection_text.ipynb

모델은 pkl파일로 따로 저장해둔다
>cloudproject_Emotion\azure_function_code\감정분류\classifymodel2.pkl

---



### azure에서 해야할 일은 두가지다
   - 일기장 내용을 받아서 감정분류 모델을 돌린 후 결과값을 반환하는 함수
   - 분류된 감정을 통하여 영화를 추천하는 함수

> get post를 통하여 데이터를 주고받아야하기 때문에 **http트리거**를 사용하여 함수앱을 구성한다



---

### azure 함수

- 감정분류
  >cloudproject_Emotion\azure_function_code\감정분류\classify_model.py
  >https://func-20202010.azurewebsites.net


  --> 입력 :  (json형식)

   {"data":[["this is amazing, I love it","his is amazing, I love it","today is awful day", " now im feel bad"]]}

  --> 출력  :  (json형식)
  
  ![Untitled](https://github.com/user-attachments/assets/7cb6df2b-6583-4735-97a3-6399d5aaddb2)



  ![image](https://github.com/user-attachments/assets/b3b5272e-0480-417b-92a4-88c4526ce8d5)


  

- 영화추천
  > cloudproject_Emotion\azure_function_code\영화추천\function_app.py
  > https://mvrecommendapp.azurewebsites.net/api/RecommendMovies?code=4VnoHjDQOkKLvSvTpm-M3pY25pBKDwnNda4kSIoKCvn_AzFu-1TGjQ==
  
  --> 입력

{
"type": "2",
"emotion": "negative"
}

  (여기서 type은 우울할때 즐거운 영화를 보는지, 우울할때 우울한 영화를 보는지 나타낸다)



--> 출력

["Airplane!","Mr. & Mrs. Smith","Zathura: A Space Adventure","The 40 Year Old Virgin","Good Morning, Vietnam","Slacker","Bride & Prejudice","Jay and Silent Bob Strike Back","Hamlet 2","Jungle Shuffle"]


![image](https://github.com/user-attachments/assets/a2dd4268-9d67-4220-b1b1-75075e821e22)




---

## 데이터 흐름

- 필요한 화면
  - 로그인
  - 회원가입
  - 게시판
  - 일기장
  - 감정분류 결과 & 영화추천


![image](https://github.com/user-attachments/assets/d2b52fdc-3f93-4eae-a2cf-41c3eea94ca3)

![image](https://github.com/user-attachments/assets/3e59adb4-389b-472d-afe8-67ff28890717)

![image](https://github.com/user-attachments/assets/3e46bf25-ca37-4eba-beb2-0f71d6af1d75)

![image](https://github.com/user-attachments/assets/126aa74a-27ec-40b8-a19d-958d4ee2496f)

![image](https://github.com/user-attachments/assets/f88a834e-6c7a-4d0b-bdad-817260f6305c)


- 필요한 table
   - 


#### 시연영상
#### https://www.youtube.com/watch?v=2mlTB_skqE4&t=6s
