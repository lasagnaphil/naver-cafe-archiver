# naver-cafe-archiver

A web-crawler/archiver for NAVER cafe (Work in progress)

네이버 카페를 아카이빙하기 위한 도구

# Install

virtualenv 혹은 conda를 사용하는 것을 권장.

설치해야 할 패키지들: selenium, bs4, sqlite3

selenium 설정은 https://selenium-python.readthedocs.io/installation.html 에서 1.1 ~ 1.4 참조.

# TODO

- [x] 로그인 (현재는 수동으로 해야함)
- [x] 크롤링
    - [x] 기초적인 파싱 (제목, 작가, 내용 텍스트)
    - [ ] 이미지/동영상 다운로드
    - [ ] 첨부파일 다운로드
- [ ] 저장
    - [ ] 글 내용을 보기 좋은 HTML로 가공
    - [ ] 파일 단위로 덤프
    - [ ] SQLite 덤프
    - [ ] JSON 덤프
