import os
import time
import scipy.io
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sklearn.externals 
import joblib
from pathlib import Path

percent=0

def export_model(mode=None):
    # # Google 주소 숫자 인식 모델 생성
    # # Path 설정
    # ml_dir = str(Path(__file__).parent)
    # md_dir = str(Path(__file__).parent.parent)
    #
    # # 로드 mat 파일
    # train_data = scipy.io.loadmat(ml_dir + '/extra_32x32.mat')
    #
    # # 학습 데이터, 훈련 데이터
    # X = train_data['X']
    # y = train_data['y']
    #
    # # 매트릭스 1D 변환
    # X = X.reshape(X.shape[0] * X.shape[1] * X.shape[2], X.shape[3]).T
    # y = y.reshape(y.shape[0], )
    #
    # # 셔플(섞기)
    # X, y = shuffle(X, y, random_state=42)
    #
    # # 학습 훈련 데이터 분리
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    #
    # # 랜덤 포레스트 객체 생성 및 학습
    # clf = RandomForestClassifier()
    # clf.fit(X_train, y_train)
    #
    # # 모델 저장(첫 학습, 재 학습 구분)
    # if not mode:
    #     joblib.dump(clf, md_dir + '/model/model.pkl')
    # else:
    #     if os.path.isfile(md_dir + '/model/model.pkl'):
    #         os.rename(md_dir + '/model/model.pkl', md_dir + f'/model/model_{time.time()}.pkl')
    #     joblib.dump(clf, md_dir + '/model/model.pkl')

    global percent
    percent=0
    while percent<=100:
        percent=percent+1
        time.sleep(0.5)

if __name__ == "__main__":
    export_model()
