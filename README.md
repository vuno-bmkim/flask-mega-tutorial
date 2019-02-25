# flask-mega-tutorial
Working through https://blog.miguelgrinberg.com/


### 1. 배포 사항
* AWS EC2 : https://18.219.79.232 (단, self-signed SSL certificate 여서 웹브라우저 경고 노출됨 & instance 메모리 이슈로 ElasticSearch 기능 제외함)
* 추가 작업 진행한 것 : Babel 한글화
        
### 2. Flask 관련 정리
* ```@app.shell_context_processor```를 통해 컨텍스트를 설정하여 flask shell을 보다 효과적으로 사용할 수 있다. 
* .flaskenv 파일을 통해 .env 파일과 구분하여 flask 관련 환경변수 정보 (ex: ```FLASK_APP```, ```FLASK_DEBUG```)만 설정할 수 있다. 
* ```app > __init__.py``` 파일에 기능별 모듈 (ex: main, auth, api, errors)과 확장 기능 (ex: db, elastic search, redis 등), 공통 정보 (ex: 비로그인자 화면, 언어) 등을 등록한다. (Django ```settings.py``` 에 대응)
* ```@app.cli.group()``` 과 ```@translate.command()``` 로 함수 정의하여 빈번히 사용되는 명령어 묶음 유틸화가 가능하다.  
* 기능별 모듈화를 위해 ```flask.Blueprint``` 를 사용한다.
* Model 필드 중 검색가능한 필드를 표현하기 위해 ```__searchable__```을 이용한다. 
* One-to-one 관계 표현을 위해 ```db.relationship```을 사용하고, many-to-many 관계 표현을 위해 ```db.relationship```과 ```db.Table()```를 사용한다. 
* 인증 필요 url 지정, 인증안된 경우 보낼 페이지 설정, 로그인 상태 정보 저장 등의 기능 사용을 위해 flask_login을 사용한다. (Django django.contrib.auth에 대응)
* API에는 적용할 수 없으나 web-only 서비스의 경우 flask가 제공하는 ```forms.py```를 사용하면 validator 구현, 웹프론트엔드 구현, form 관련 초기화 로직 구현 (ex: 프론트에서 보여질 디폴트값 설정 ) 등에 용이하다. 
* 백엔드 처리 결과/오류 등을 프론트엔드에서 보여주는 것 관련하여 flask flash를 사용할 수 있다.
* ```@app.errorhandler``` (Flask 클래스), ```@bp.app_errorhandler``` (BluePrint 클래스)를 사용해 특정 에러코드에 대한 로직 구현 및 렌딩 페이지 일괄 설정 이 가능하다.
* ```get_or_404()```, ```first_or_404()``` 쿼리를 이용해서 대응하는 데이터 존재하지 않는 경우 바로 404 (File not found)에러 발생시키는 로직을 간소화할 수 있다.
    
    
### 3. 패턴/컨벤션 관련 정리
* 재사용되는 유틸성 기능 관리시 아래 4가지 방법을 통해 연관된 데이터와 함수의 응집성을 높이고, 재사용성을 높일 수 있다. 
    1) 특정 Model/Form 인스턴스에 대한 기능일 경우 해당 클래스 인스턴스 메소드 형태로 구현
    2) 특정 Model과 연관이 있으나 인스턴스를 사용하지 않는 경우 (ex: User 모델과 연관된 기능이나 user 인스턴스를 사용하지 않는 ```verify_token(token)```)에는 정적 메소드 형태로 구현 (```@staticmethod```, ```@classmethod```)
    3) 여러 Model에 공통적으로 사용될 수 있는 기능인 경우 (ex: 페이지네이션 가능한 API용 ```to_collection_dict()```, 검색 가능한 데이터용 ElasticSearch 추가/조회 기능) Mixin을 이용해 재사용
    4) 외부 라이브러리 사용 관련 유틸성 기능 (ex: 이메일 발송, ElasticSearch 관련, Microsoft translator API 관련, Redis Queue 관련 등) 의 경우 따로 파일 생성하여 처리 
* REST API 개념 (self-descriptive message, hypermedia as the engine of application state)을 보다 충실히 따르기 위해 API 데이터에 ```_meta```, ```_links``` 정보를 포함시킨다. 
* 각 환경 (로컬, 테스트 서버, 프로덕션 서버 등)별로 달라야 하는 정보 (ex: db uri, elasticsearch url 등)를 기본적으로는 환경변수로 처리하여 git에 공유되지 않고 각 환경별로 존재하도록 하고, 개발시에 편의를 위해 .env 파일을 통해 변경한다. 
* 컴포넌트로 활용되는 html 명시를 위해 해당 html 파일 앞에 _ (underbar)를 붙인다. 
* Token expiration 필드를 두어 정기적으로 인증 token 정보를 갱신한다. 
