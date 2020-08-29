#텍스트 클리닝과 텍스트 토큰화
#from konlpy.tag import Okt 보통의 경우에는 Okt를 사용하지 x
import json
import os
import re
from pprint import pprint
import rhinoMorph
from collections import Counter
import pandas as pd
import math

from tensorflow.compat.v2.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
max_words = 5000
max_len = 100

rn = rhinoMorph.startRhino()

# 텍스트 클리닝 - 한글만 남기기
def text_cleaning(doc):
    
    doc = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", doc)
        
    return doc

# 불용어 정의
def define_stopwords(path, encoding):
    
    SW = set() 
    #집합형태로 만들어줘야 중복을 제외하고 출력해줌
    #불용어들을 추가할려면 SW.add()이렇게 넣어주면 됨
    
    with open(path, encoding = encoding) as f:
        for word in f:
            SW.add(word)
            
    return SW

# 모델 로딩
def load_model():
    json_file = open("application/model/NLP_model.json", "r") 
    loaded_model_json = json_file.read()
    json_file.close() 

    # json파일로부터 model 로드하기 
    loaded_model = model_from_json(loaded_model_json) 

    # 로드한 model에 weight 로드하기 
    loaded_model.load_weights("application/model/NLP_weight.h5")

    return loaded_model

SW = define_stopwords("application/model/stopwords-ko.txt", encoding = 'utf-8')
tokenizer = joblib.load('application/model/tokenizer.pickle')
# def text_tokenizing(doc):
#     return [word for word in rhinoMorph.onlyMorph_list(rn,doc, pos = ['NNG', 'NNP','NP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'], eomi = False) if word not in SW and len(word) > 1]

# 분석!!!
def sentiment_predict(new_sentence):
    score = 0
    model = load_model()
    if new_sentence != '':
        new_sentence1 = text_cleaning(new_sentence)
        new_sentence2 = rhinoMorph.onlyMorph_list(rn,new_sentence1, pos = ['NNG', 'NNP','NP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'], eomi = False)
        new_sentence3 = [word for word in new_sentence2 if not word in SW] # 불용어 제거
        encoded = tokenizer.texts_to_sequences([new_sentence3]) # 정수 인코딩
        if encoded != [[]]:
            pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
            score = float(model.predict(pad_new))
    return score
