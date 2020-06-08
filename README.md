# [Rank42](https://rank42.herokuapp.com/)
![Python](https://img.shields.io/badge/python-3.7.7-green)
![Django](https://img.shields.io/badge/django-2.2.13-blue)

## 소개
42 Seoul의 랭킹 관련 웹서비스 입니다.  
더 자세한 내용은 위키를 확인해주세요!  

## 개발환경
- Python 3.7.7  
- Django 2.2.13  
- Sqlite3(개발용), PostgreSQL(프로덕션용)  
- Pycharm IDE  

## 실행방법
"/rank42/config/settings" 경로에 'secret_info_file.json'파일이 필요합니다. 아래와 같은 형태의 JSON 파일입니다.  

```json
{
  "FT_UID_KEY": "UID KEY",
  "FT_SECRET_KEY": "SECRET KEY"
}
```

> 42Api 키발급은 [https://profile.intra.42.fr/oauth/applications](https://profile.intra.42.fr/oauth/applications)에서 'REGISTER A NEW APP'을 통해 가능합니다.

## 폴더설명
- .idea : Pycharm IDE 관련 설정  
- api_test : 42api 관련 테스트 코드(사실상 낙서장)  
- rank42 : Rank42 관련 코드  
