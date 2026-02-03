# FastAPI for Spring Developers

이 프로젝트는 **Spring Framework**에 익숙한 개발자가 **FastAPI**를 쉽게 학습하고 적응할 수 있도록, Spring의 계층형 아키텍처(Controller-Service-Repository)를 적용한 예제 프로젝트입니다.

## 🏗 아키텍처 및 구조 (Spring vs FastAPI)

Spring의 주요 개념을 FastAPI의 컴포넌트로 매핑하여 구성했습니다.

| Spring Concept | FastAPI Implementation | 파일 위치 | 역할 |
| :--- | :--- | :--- | :--- |
| **DataSource** | `sqlalchemy.create_engine` | `app/db/session.py` | DB 연결 및 세션 관리 |
| **@Entity** | `Base` (SQLAlchemy) | `app/models/` | 데이터베이스 테이블 매핑 |
| **JpaRepository** | Repository Class | `app/repositories/` | 데이터 접근 계층 (DAO) |
| **DTO** | `Pydantic BaseModel` | `app/schemas/` | 데이터 전송 객체 & 유효성 검사 |
| **@Service** | Service Class | `app/services/` | 비즈니스 로직 처리 |
| **@RestController** | `APIRouter` | `app/api/v1/endpoints/` | API 엔드포인트 정의 |
| **@Autowired** | `Depends(...)` | (각 함수의 인자) | 의존성 주입 (DI) |
| **application.yml** | `BaseSettings` | `app/core/config.py` | 환경 설정 관리 |

### 📂 디렉토리 구조
```text
app/
├── main.py              # SpringApplication.run() - 앱 진입점 및 설정
├── core/
│   └── config.py        # 설정 파일 (환경변수 등)
├── db/
│   └── session.py       # DB 세션 및 연결 설정
├── models/              # DB 엔티티 (ORM)
├── schemas/             # DTO (Request/Response 모델)
├── repositories/        # DB 액세스 로직
├── services/            # 비즈니스 로직
└── api/
    └── v1/
        ├── api.py       # 라우터 모음
        └── endpoints/   # 개별 컨트롤러
```

## 🛠 기술 스택

*   **Language**: Python 3.12+
*   **Web Framework**: FastAPI
*   **ORM**: SQLAlchemy (JPA 역할)
*   **Validation**: Pydantic
*   **Server**: Uvicorn (Tomcat/Netty 역할)
*   **Database**: SQLite (기본 설정, 파일로 저장됨)

## 🚀 시작하기 (Getting Started)

### 1. 환경 설정 및 설치

가상 환경을 활성화하고 의존성을 설치합니다.

```bash
# 가상환경 활성화 (이미 되어 있다면 생략)
source .venv/bin/activate

# 라이브러리 설치
pip install -r requirements.txt
```

### 2. 서버 실행

프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
# 개발 모드 (코드 변경 시 자동 재시작)
uvicorn app.main:app --reload
```

또는 `main.py`를 직접 실행할 수도 있습니다.

```bash
python main.py
```

### 3. API 테스트

서버가 실행되면 다음 주소에서 자동 생성된 API 문서를 확인할 수 있습니다.

*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📝 주요 기능

*   **회원가입 (Create)**: `POST /api/v1/users/`
*   **회원 목록 조회 (Read)**: `GET /api/v1/users/`
*   **회원 상세 조회 (Read)**: `GET /api/v1/users/{user_id}`

DB는 실행 시 `sql_app.db` 파일로 자동 생성되며, `app/main.py`에서 테이블 자동 생성 로직(`Base.metadata.create_all`)이 동작합니다.
