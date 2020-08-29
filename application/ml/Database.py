import cx_Oracle
import os
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import geocoder

os.environ["NLS_LANG"] = ".AL32UTF8"
location_list = ['경기', '강원', '경상남도', '경상북도', '충청남도', '충청북도', '전라남도', '전라북도', '제주특별자치도', '대전', '광주', '부산', '울산', '대구', '인천']


# sql = 'select LOCAL_ID from tempdata where local_id = ' + "'수지구'"
sql = 'select * from child_0 where 아동_성별 = ' + "'M'"

# cursor.execute(sql.encode('utf-8'))



def print_db():
    print("test1")
    cursor.execute(sql.encode('utf-8'))
    for row in cursor:
        print(row)
    print("test2")

# def read_database(case_num, child_id):
#     sql_read = "select * from child_0 where 개별사건번호 = '%d' and 피해아동대상자 = '%s'" %(int(case_num), child_id)
#     row = cursor.execute(sql_read.encode('utf-8'))
#     db_data = row.fetchone()
#     return db_data


    # locator = Nominatim(user_agent = "myGeocoder")
    # coordinates = "%f, %f" % (myloc.latlng[0], myloc.latlng[1])
    # location = locator.reverse(coordinates, language=RFC2616)
    # temp_province = location.raw['address']['province']

    # if()
def read_database():
    #DB 연결
    conn = cx_Oracle.connect("Jason/ssis1234@localhost:49161/xe")
    cursor = conn.cursor()

    #위치정보
    myloc = geocoder.ip('me')
    locator = Nominatim(user_agent = "myGeocoder")
    coordinates = "%s, %s" %(myloc.latlng[0], myloc.latlng[1])
    print(coordinates)
    location = locator.reverse(coordinates)
    my_location = None
    
    try:
        my_location = location.raw['address']['city']
    except(KeyError):
        pass
    try:
        my_location = location.raw['address']['province']
    except(KeyError):
        pass

    for i in range(len(location_list)):
        if my_location != location_list[i]:
            if (myloc.latlng[0] >= 37.413294 and myloc.latlng[0] <= 37.715133) and (myloc.latlng[1] >= 126.734086 and myloc.latlng[1] <= 127.269311):
                my_location = '서울'
            elif(myloc.latlng[0] >= 36.418608 and myloc.latlng[0] <= 36.733585) and (myloc.latlng[1] >= 127.126739 and myloc.latlng[1] <= 127.409310):
                my_location = '세종'    
    if my_location == '경기도':
        my_location = '경기'
    elif my_location == '경상남도':
        my_location = '경남'
    elif my_location == '경상북도':
        my_location = '경북'
    elif my_location == '충청남도':
        my_location = '충남'
    elif my_location == '충청북도':
        my_location = '충북'
    elif my_location == '전라남도':
        my_location = '전남'
    elif my_location == '전라북도':
        my_location = '전북'
    elif my_location == '제주특별자치도':
        my_location = '제주'
    
    #날짜정보
    # case_num = request.form['case_num']
    # child_id = request.form['child_id']
    todayDate = datetime.now()
    # todayDate = tempDate.strftime('%Y-%m-%d')

    threeMonthBefore = todayDate - timedelta(days=820)
    sixMonthBefore = todayDate - timedelta(days=910)

    # 소문자 y -> 20, 대문자 Y -> 2020
    tMB_Date = threeMonthBefore.strftime('%y-%m-%d')
    sMB_Date = sixMonthBefore.strftime('%y-%m-%d')
    # db_data = db.read_database(case_num, child_id)

    tMB_Date = tMB_Date.replace('-', '/')
    sMB_Date = sMB_Date.replace('-', '/')

    # sql_read = """select * from child_0 
    #             where (신고_통보일시 <= TO_DATE('%s', 'YY/MM/DD') and 신고_통보일시 >= TO_DATE('%s', 'YY/MM/DD')
    #             and 신대_통계거점 = '%s' and 결과_학대혐의여부 = 'Y')""" %(tMB_Date, sMB_Date, my_location)
    sql_read = """select 개별사건번호, 피해아동대상자, 학대행위자대상, 신대_통계거점, 결과_학대혐의여부 from child_0 
                where (신고_통보일시 <= TO_DATE('%s', 'YY/MM/DD') and 신고_통보일시 >= TO_DATE('%s', 'YY/MM/DD')
                and 신대_통계거점 = '%s')""" %(tMB_Date, sMB_Date, my_location)
    row = cursor.execute(sql_read.encode('utf-8'))
    db_data = row.fetchall()
    conn.close()

    return db_data