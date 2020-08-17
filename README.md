# [Rank42](https://rank42.herokuapp.com/)
![Python](https://img.shields.io/badge/python-3.8.5-green)
![Django](https://img.shields.io/badge/django-3.1-blue)

## 소개
42 Seoul의 랭킹 관련 웹서비스 입니다.  
더 자세한 내용은 위키를 확인해주세요!  

## 개발환경
- Python 3.8.5  
- Django 3.1  
- Sqlite3(개발용), PostgreSQL(프로덕션용)  
- Pycharm IDE  

## 실행방법
"/rank42/config/settings" 경로에 'secret_info_file.json'파일이 필요합니다. 아래와 같은 형태의 JSON 파일입니다.  

```json
{
  "FT_UID_KEY": "42 API UID KEY",
  "FT_SECRET_KEY": "42 API SECRET KEY"
}
```
> 상세한 방법은 [wiki의 기여 가이드](https://github.com/progresshans/rank42/wiki/기여-가이드)를 통해 확인할 수 있습니다.
> 42Api 키발급은 [https://profile.intra.42.fr/oauth/applications](https://profile.intra.42.fr/oauth/applications)에서 'REGISTER A NEW APP'을 통해 가능합니다.

## 폴더설명
- .idea : Pycharm IDE 관련 설정  
- api_test : 42api 관련 테스트 코드(사실상 낙서장)  
- rank42 : Rank42 관련 코드  

## 기여는 언제나 환영입니다!
Rank42에 기여하고 싶으신가요? [위키](https://github.com/progresshans/rank42/wiki)를 통해 [기여 가이드](https://github.com/progresshans/rank42/wiki/기여-가이드)와 [개발 배경 및 방향](https://github.com/progresshans/rank42/wiki/개발-배경-및-방향)을 살펴보세요!
