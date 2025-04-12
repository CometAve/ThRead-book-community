# ThRead - 독서 커뮤니티 플랫폼

<div align="center">
  <img src="assets/프로젝트 메인화면.png" alt="ThRead 대표 이미지" width="300">
  <p><i>Django 웹 프레임워크를 활용한 개인 학습 목적의 도서 커뮤니티 플랫폼</i></p>
</div>

## 📚 프로젝트 소개

**ThRead**는 Django 기반으로 개발된 독서 커뮤니티 및 도서 관리 웹 애플리케이션입니다. 사용자가 개인 서재를 관리하고, 독서 기록을 남기며, 다른 독자들과 서평과 생각을 공유할 수 있는 플랫폼입니다. 이 프로젝트는 Python과 Django 프레임워크를 공부하며 웹 개발 역량 향상을 위한 개인 학습 목적으로 진행되었습니다. 추후 RESTful API와 Vue.js를 익혀 프로젝트에 녹여낼 예정입니다.

### 개발 기간
- 2025년 3월 ~ 2025년 5월

## 🛠 기술 스택

### 백엔드
- **언어 & 프레임워크:** Python 3.13, Django
- **데이터베이스:** SQLite3
- **인증 시스템:** Django Authentication

### 프론트엔드
- **템플릿 엔진:** Django Template
- **스타일링:** CSS, Bootstrap
- **인터랙션:** JavaScript, AJAX

### API 통합
- OpenAI API (TTS 기능 구현)

## ✨ 주요 기능

### 사용자 관리
- **커스텀 사용자 모델**: 사용자 프로필 확장 (연령, 성별, 관심 장르)
- **인증 시스템**: 회원가입, 로그인, 프로필 관리
- **비밀번호 변경**: 사용자 계정 보안 강화(개선 필요)

### 도서 관리
- **도서 CRUD**: 도서 등록, 조회, 수정, 삭제 기능
- **카테고리 분류**: 장르별 도서 분류
- **검색 기능**: 제목, 작가 기반 도서 검색

### 커뮤니티
- **서평 공유**: 사용자들이 읽은 책에 대한 리뷰 공유
- **개인 서재 관리**: 사용자별 읽은 책, 관심 책 관리

### 미디어 처리
- **이미지 업로드**: 도서 표지, 작가 프로필, 사용자 프로필 이미지 관리
- **TTS (Text-to-Speech)**: OpenAI API를 통해 텍스트를 음성으로 변환하는 기능

## 🌟 학습 내용

1. **Django ORM 활용**: 복잡한 데이터 관계 모델링 및 쿼리 최적화 학습
2. **사용자 인증 및 권한 관리**: Django의 인증 시스템 커스터마이징
3. **파일 업로드 및 미디어 처리**: 이미지와 오디오 파일의 효율적 관리
4. **외부 API 연동**: OpenAI API를 활용한 TTS 기능 구현
5. **비동기 처리**: AJAX를 활용한 도서 검색 및 결과 표시
6. **반응형 웹 디자인**: 다양한 디바이스에 최적화된 UI/UX 구현

## 📋 ERD(Entity Relationship Diagram)

```
User(사용자) ---- N:M ---- Book(도서)
    |               |
    |               |
    v               v
Profile(프로필)   Category(카테고리)
```

## 🚀 설치 및 실행 방법

1. 저장소 클론
```bash
git clone https://github.com/CometAve/ThRead-book-community.git
cd ThRead
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

4. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

5. 개발 서버 실행
```bash
python manage.py runserver
```

6. 웹 브라우저에서 접속: `http://127.0.0.1:8000/`

## 📷 스크린샷

(스크린샷 이미지들이 들어갈 위치입니다)

## 🔜 향후 개선 계획

- 소셜 로그인 기능 추가
- 도서 리뷰 분석을 위한 자연어 처리 기능 구현
- 독서 모임 일정 관리 기능
- 사용자 맞춤 도서 추천 시스템

## 📝 학습 후기 및 회고

** 목표한 기술까지 최종적으로 학습하고 프로젝트에 녹여낸 후 작성 예정입니다. **
<!-- 이 프로젝트는 Django 프레임워크를 활용한 웹 개발의 전반적인 이해를 돕기 위해 진행되었습니다. MVC 아키텍처의 이해, 데이터베이스 모델링, 사용자 인증 및 권한 관리, 미디어 파일 처리, 외부 API 연동 등 다양한 웹 개발 기술을 학습하고 적용해볼 수 있었습니다.

특히 Django의 강력한 ORM 기능과 인증 시스템을 활용하면서 많은 것을 배웠으며, 프론트엔드와 백엔드를 아우르는 풀스택 개발 경험을 쌓을 수 있었습니다. 이 프로젝트는 웹 개발자로서의 역량을 한층 더 높이는 귀중한 경험이 되었습니다. -->

## 👨‍💻 개발자 정보

- LinkedIn: [linkedin.com/in/hyeseongro](https://www.linkedin.com/in/hyeseongro/)
- GitHub: [github.com/CometAve](https://github.com/CometAve)

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.