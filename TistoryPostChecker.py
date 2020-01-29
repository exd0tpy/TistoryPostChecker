#-*- coding:utf-8 -*-
import requests
import json
import sys


'''

필수 기입 정보

'''
#티스토리 api토큰 생성을 위한 정보
ID = '아이디(이메일)'
PASS = '비밀번호'
BLOGNAME = '블로그이름'   #xxx.tistory.com에서 xxx부분입니다.


#로그 폰트 관련
C_END     = "\033[0m"
C_BOLD    = "\033[1m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
info_head_star = "["+C_BOLD + C_GREEN+"*"+C_END+"] "
info_head_plus = "["+C_BOLD + C_GREEN+"+"+C_END+"] "
info_head_minus = "["+C_BOLD + C_RED+"-"+C_END+"] "


#티스토리 토큰 받아오기
def tistory_auth():
    session = requests.session()

    loginInfo = { "redirectUrl":"http://dev-pengun.tistory.com", "loginId" : ID, "password" : PASS, "rememberLoginId":"1", "fp":"70bc1830ac2441e5abe054ab760b0af6" } 
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7", "Origin":"https://www.tistory.com", "Referer":"https://www.tistory.com/auth/login", "Cache-Control":"max-age=0", "Upgrade-Insecure-Requests":"1", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36" } 
    url_login = "https://www.tistory.com/auth/login" 
    res = session.post(url_login, data=loginInfo, headers =headers)
    
    TISTORY_APPID = '09ee5023123aa00ab0273adfe9086afa'

    params = {
    'client_id' : TISTORY_APPID,
    'redirect_uri' : "http://dev-pengun.tistory.com",
    'response_type' : 'token',
    }   

    host = 'https://www.tistory.com/oauth/authorize'
    res = session.get(host, params=params)
    try:
        token =  res.url.split('access_token=')[1].split('&')[0]
    except:
        print ("메일함에서 로그인 인증을 해주세요")
        sys.exit()

#구글에서 검색결과가 첫 페이지에 표시되는지 체크
def searchGoogle(title):
    host = 'https://www.google.com/search'
    params = {
        'q' : title
    }
    res = requests.get(host,params=params)
    res = res.text.find(BLOGNAME)
    if res == -1:
        return False
    else:
        return True

#네이버에서 검색결과가 첫 페이지에 표시되는지 체크
def searchNaver(title):
    host = 'https://search.naver.com/search.naver'
    params = {
        'query' : title
    }
    res = requests.get(host,params=params)
    res = res.text.find(BLOGNAME)
    if res == -1:
        return False
    else:
        return True

#다음에서 검색결과가 첫 페이지에 표시되는지 체크
def searchDaum(title):
    host = 'https://search.daum.net/search'
    params = {
        'q' : title
    }
    res = requests.get(host,params=params)
    res = res.text.find(BLOGNAME)
    if res == -1:
        return False
    else:
        return True


#결과를 출력하는 함수
def printSearchResult(titles):
    print('\n' + info_head_star + '공개된 포스트 수 : ' + str(len(titles)) + '\n')

    googleFlag = False
    naverFlag = False
    daumFlag = False
    notSearchable = []

    for title in titles:
        print(info_head_star + title) 

        if searchGoogle(title):
            print('\t' + info_head_plus + '구글에서 검색됨.')
        else:
            notSearchable.append({'Google' : title})
            googleFlag = True
            print('\t' + info_head_minus + '구글에서 검색안됨.')

        if searchDaum(title):
            print('\t' + info_head_plus + '다음에서 검색됨.')
        else:
            notSearchable.append({'Daum' : title})
            daumFlag = True
            print('\t' + info_head_minus + '다음에서 검색안됨.')

        if searchNaver(title):
            print('\t' + info_head_plus + '네이버에서 검색됨.')
        else:
            notSearchable.append({'Naver' : title})
            naverFlag = True
            print('\t' + info_head_minus + '네이버에서 검색안됨.')
        print('')

    if notSearchable:
        if googleFlag:
            print(info_head_star + '구글 검색이 안되는 포스트 : ')
            for item in notSearchable:
                if 'Google' in item:
                    print('\t' + item['Google'])
        if daumFlag:
            print(info_head_star + '다음 검색이 안되는 포스트 : ')
            for item in notSearchable:
                if 'Daum' in item:
                    print('\t' + item['Daum'])
        if naverFlag:
            print(info_head_star + '네이버 검색이 안되는 포스트 : ')
            for item in notSearchable:
                if 'Naver' in item:
                    print('\t' + item['Naver'])

    else:
        print(info_head_star + '모든 포스트가 정상적으로 검색됩니다.')


#티스토리 api를 이용해서 공개 발행된 포스트의 타이틀을 받아오기
def getPostTitle(authCode):
    titles = []
    page = 1
    while(True):
        params = {
            'access_token' : authCode,
            'output': 'json',
            'blogName': BLOGNAME,
            'page' : page,
        }
        host = 'https://www.tistory.com/apis/post/list'
        res = requests.get(host,params=params)
        try:
            for item in json.loads(res.text)['tistory']['item']['posts']:
                if item['visibility'] == '20':
                    titles.append(item['title'])
        except:
            break
        page += 1

    return titles



titles  = getPostTitle(tistory_auth())
printSearchResult(titles)
