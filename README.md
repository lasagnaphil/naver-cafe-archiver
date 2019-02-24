# naver-cafe-archiver

A web-crawler/archiver for NAVER cafe (Work in progress)

네이버 카페를 아카이빙하기 위한 도구

# Install

- 파이썬 3.7+에서 구동. 현재로서는 리눅스에서만 테스트해봄.

- 설치해야 할 패키지들: selenium, bs4, peewee, tqdm
    - 패키지 설치는 virtualenv 혹은 conda를 사용하는 것을 권장.

- selenium 설정은 https://selenium-python.readthedocs.io/installation.html 에서 1.1 ~ 1.4 참조.

# TODO

- [x] 로그인 (현재는 수동으로 해야함)
- [x] 크롤링
    - [x] 기초적인 파싱 (제목, 작가, 내용 텍스트)
    - [ ] 이미지/동영상 다운로드
    - [ ] 첨부파일 다운로드
- [ ] 저장
    - [x] SQLite로 저장
    - [ ] JSON 덤프
- [ ] 서버
    - [ ] Flask를 통해 웹페이지로 데이터 보기
