from flask import Blueprint, request, render_template, flash, redirect, url_for, Response, Flask
from flask import current_app as app
import flask
import sklearn.externals 
import joblib
import numpy as np
import imageio
from scipy import misc

import application.ml.model as MM #모델재학습 연동
import application.ml.NLP as nlp #자연어처리 연동
import application.ml.Database as db #데이터베이스 연동

from werkzeug.utils import secure_filename

from flask_restful import Resource, Api
import pandas as pd
import folium
import webbrowser
import time
import random
import xgboost as xgb

app = Flask(__name__)
# 추가할 모듈이 있다면 추가
 
main = Blueprint('main', __name__, url_prefix='/')

api = Api(main)


xgb_model = joblib.load('application/model/XGBOOST.pkl')
forest_model = joblib.load('application/model/FOREST.pkl')

diary_temp_text = ''
data_columns = ['아동정보.성별_F', '아동정보.성별_M', '아동정보.거주상태_기타', '아동정보.거주상태_무상', '아동정보.거주상태_보증금(전세)+월세', '아동정보.거주상태_보호시설', '아동정보.거주상태_영구임대아파트  또는 영구임대주택',
 '아동정보.거주상태_월세', '아동정보.거주상태_자택', '아동정보.거주상태_전세', '아동정보.가족 유형_기타', '아동정보.가족 유형_동거(사실혼포함)', '아동정보.가족 유형_모자가족(가출)', '아동정보.가족 유형_모자가족(별거)', 
 '아동정보.가족 유형_모자가족(사별)', '아동정보.가족 유형_모자가족(이혼)', '아동정보.가족 유형_미혼부·모가정', '아동정보.가족 유형_부자가족(가출)', '아동정보.가족 유형_부자가족(별거)', '아동정보.가족 유형_부자가족(사별)',
  '아동정보.가족 유형_부자가족(이혼)', '아동정보.가족 유형_소년소녀가정', '아동정보.가족 유형_시설보호', '아동정보.가족 유형_위탁가정', '아동정보.가족 유형_입양가정', '아동정보.가족 유형_재혼가정', '아동정보.가족 유형_친부모가정', 
  '아동정보.가족 유형_친인척보호', '아동정보.가구 소득 구분코드_100만원이상-150만원미만', '아동정보.가구 소득 구분코드_150만원이상-200만원미만', '아동정보.가구 소득 구분코드_200만원이상-250만원미만', 
  '아동정보.가구 소득 구분코드_250만원이상-300만원미만', '아동정보.가구 소득 구분코드_300만원이상', '아동정보.가구 소득 구분코드_50만원미만', '아동정보.가구 소득 구분코드_50만원이상~100만원미만', '아동정보.기초생활수급 유형_비수급권대상', 
  '아동정보.기초생활수급 유형_수급권대상', '신고접수.재신고 유형_동일센터 사례종결후 재신고', '신고접수.재신고 유형_사례진행중 재신고', '신고접수.재신고 유형_일반상담 후 재신고', '신고접수.재신고 유형_타센터 사례종결후 재신고', 
  '신고접수.신고접수 구분_경찰접수', '신고접수.신고접수 구분_아동보호전문기관접수', '신고접수.피해아동 상태 구분_아동사망', '신고접수.피해아동 상태 구분_중상해(의식불명 포함)', '신고접수.피해아동 상태 구분_해당사항없음', 
  '신고접수(대상자관계).아동 동거 여부_동거', '신고접수(대상자관계).아동 동거 여부_비동거', '신고접수(대상자관계).재신고 여부_N', '신고접수(대상자관계).재신고 여부_Y', '신고접수(대상자관계).통계 거점_강원', 
  '신고접수(대상자관계).통계 거점_경기', '신고접수(대상자관계).통계 거점_경남', '신고접수(대상자관계).통계 거점_경북', '신고접수(대상자관계).통계 거점_광주', '신고접수(대상자관계).통계 거점_대구', '신고접수(대상자관계).통계 거점_대전', 
  '신고접수(대상자관계).통계 거점_부산', '신고접수(대상자관계).통계 거점_서울', '신고접수(대상자관계).통계 거점_세종', '신고접수(대상자관계).통계 거점_울산', '신고접수(대상자관계).통계 거점_인천', '신고접수(대상자관계).통계 거점_전남', 
  '신고접수(대상자관계).통계 거점_전북', '신고접수(대상자관계).통계 거점_제주', '신고접수(대상자관계).통계 거점_중앙', '신고접수(대상자관계).통계 거점_충남', '신고접수(대상자관계).통계 거점_충북', '판단결과.학대 혐의 여부_N', 
  '판단결과.학대 혐의 여부_Y', '생년월일구분_10~12세', '생년월일구분_13~15세', '생년월일구분_16~17세', '생년월일구분_18세이상', '생년월일구분_1~3세', '생년월일구분_4~6세', '생년월일구분_7~9세']

# 메인페이지 라우팅
@app.route("/")
@app.route('/main')
def index():
      # /main/index.html은 사실 /project_name/app/templates/main/index.html을 가리킵니다.
      return render_template('/main/index.html')


# 소개페이지 라우팅
@app.route('/about')
def about():
    return render_template('/About Us/about.html')

# 결과페이지 라우팅
@app.route('/results')
def results():
    return render_template('/Maps/easy.html')

# 결과페이지 라우팅2
@app.route('/results2')
def results_2():
    return render_template('/Maps/folium_kr.html')

# 새로운 데이터 입력 페이지 라우팅
@app.route('/putData')
def putData():
    return render_template('/Test/putData.html')

# 데이터 예측 처리  
@app.route('/predict',methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        input_data = []
        data = [0 for i in range(77)]
        # 성별
        input_data.append(request.form['sex'])
        # 거주상태
        input_data.append(request.form['residence'])
        # 가족유형
        input_data.append(request.form['family'])
        # 가구소득구분코드
        input_data.append(request.form['income'])
        # 기초생활수급유형
        input_data.append(request.form['supply'])
        # 재신고유형
        input_data.append(request.form['retype'])
        # 신고접수구분
        input_data.append(request.form['receipt'])
        # 피해아동상태구분
        input_data.append(request.form['child'])
        # 아동동거여부
        input_data.append(request.form['together'])
        # 재신고여부
        input_data.append(request.form['re'])
        # 통계거점
        input_data.append(request.form['st'])
        # 학대혐의여부
        input_data.append(request.form['suspicion'])
        # 생년월일
        temp_birthday = request.form['birthday']
        if temp_birthday == '':
            birthday = None
        else:
            birthday = int(temp_birthday)
            if (2019 - (birthday/10000)) >= 0.0 and (2019 - (birthday/10000)) < 1.0:
                input_data.append('1세미만')
            elif (2019 - (birthday/10000)) >= 1.0 and (2019 - (birthday/10000)) <= 3.0:
                input_data.append('1~3세')
            elif (2019 - (birthday/10000)) >= 4.0 and (2019 - (birthday/10000)) <= 6.0:
                input_data.append('4~6세')
            elif (2019 - (birthday/10000)) >= 7.0 and (2019 - (birthday/10000)) <= 9.0:
                input_data.append('7~9세')
            elif (2019 - (birthday/10000)) >= 10.0 and (2019 - (birthday/10000)) <= 12.0:
                input_data.append('10~12세')
            elif (2019 - (birthday/10000)) >= 13.0 and (2019 - (birthday/10000)) <= 15.0:
                input_data.append('13~15세')
            elif (2019 - (birthday/10000)) >= 16.0 and (2019 - (birthday/10000)) <= 17.0:
                input_data.append('16~17세')
            else:
                input_data.append('18세이상')

        for i in range(0, len(input_data)):
            for j in range (0, len(data_columns)):
                if input_data[i] == data_columns[j]:
                    data[j] = 1

        reshape_data = np.array(data).reshape(1, 77)
        # xgb_prediction = xgb_model.predict(reshape_data)
        # xgb_label = str(np.squeeze(xgb_prediction))

        forest_prediction = forest_model.predict(reshape_data)
        forest_label = str(np.squeeze(forest_prediction))

        # # 결과 리턴
        return render_template('/Test/putData.html', ml_label=forest_label)

# 데이터 모델 재학습
@app.route('/retrain', methods=['POST'])
def make_model():
    if request.method == 'POST':
        # 모델 재 생성
        MM.export_model('R')
        return render_template('/Test/putData.html', md_label='모델 재생성 완료')

# progress bar
@app.route('/progress')
def progress():
    def generate():
        while MM.percent <= 100:
            yield "data:" + str(MM.percent) + "\n\n"
            time.sleep(0.5)

    # html은 test
    return Response(generate(), mimetype='text/event-stream')

# 데이터 모델 재학습(RestApi)
class RestMl(Resource):
    def get(self):
        MM.export_model('R')
        return {'result': True, 'modelName': 'model.pkl'}

# Rest 등록
api.add_resource(RestMl, '/retrainModel')


@app.route('/inquire', methods=['GET', 'POST'])
def inquire():
    
    page = request.args.get('page', type=int, default=1)  # 페이지
    db_data = []
    len_db_data = 0
    if request.method == 'POST':  
        db_data = db.read_database()
        len_db_data = len(db_data)
        # db_data = db_data.paginate(page, per_page = 10, total=len_db_data)
    
    # db.print_db()
    return render_template('/Test/inquire.html', inquire_results = db_data, data_length = len_db_data)

# 다이어리 입력 페이지 라우팅
@app.route('/diary', methods=['GET','POST'])
def diary():
    # NLP_predict = []
    # NLP_predict.append([])
    # global diary_temp_text
    # diary_text = 'diary'
    # NLP_results = round(random.random(), 4) * 100
    # if request.method == 'POST':
    #     diary_temp_text = request.form['diary_textarea']
    #     NLP_predict[0].append(diary_temp_text)

    #     diary_text, diary_NLP_results = nlp.preprocessing(NLP_predict)

    # else:
    if request.method == 'POST':
        diary_text = request.form['diary_textarea']
        diary_NLP_results = nlp.sentiment_predict(diary_text)

    else:
        diary_text = None
        diary_NLP_results = 0.0

    return render_template('/Diary/diary.html', diary_text = diary_text, diary_NLP_results=diary_NLP_results)
    # return redirect(url_for('main.diary_2', diary_text=temp, diary_NLP_results=0))

# # 다이어리 페이지 결과값 전달 페이지
# @main.route('/diary2')
# def diary_2(diary_text = None, diary_NLP_results=0.0):
#     #감성 분석 코드 들어가기
#     # NLP_results = diary_NLP_results
#     return render_template('/Diary/diary.html', diary_text = diary_text, diary_NLP_results=diary_NLP_results)

# 그림???
@app.route('/sketch', methods=['GET','POST'])
def sketch():
    if request.method == 'POST':
        # 업로드 파일 처리 분기
        file = request.files['image']
        sfname = 'static/images/' + str(secure_filename(file.filename))
        if not file:
            sketch_text ='No Files'
            return render_template('/Sketch/sketch.html', label=sketch_text)
        else:
            sketch_text = '제출완료'
            return render_template('/Sketch/sketch.html', label=sketch_text, imgpath=sfname)

        # 이미지 픽셀 정보 읽기
        # 알파 채널 값 제거 후 1차원 Reshape
        # img = misc.imread(file)
        # img = img[:, :, :3]
        # img = img.reshape(1, -1)

        # 입력 받은 이미지 예측
        # prediction = model.predict(img)

        # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환
        # label = str(np.squeeze(prediction))

        # 숫자가 10일 경우 0으로 처리
        # if label == '10': label = '0'

        # 결과 리턴
    return render_template('/Sketch/sketch.html')


if __name__ == "__main__":
    app.debug = True

    app.run(host = "127.0.0.1", port = 5050)
