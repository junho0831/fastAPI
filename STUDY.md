# 🧪 FastAPI 실습 가이드 (Spring 개발자용)

퀴즈로 냈던 3가지 상황을 직접 실험해보고 결과를 확인할 수 있는 가이드입니다.

## 0. 준비 (데이터 생성)
서버를 실행하고 아래 명령어로 실습용 데이터를 생성하세요.
(또는 Swagger UI에서 `/study/setup` 호출)

```bash
curl -X POST http://localhost:8000/study/setup
```

---

## 🔬 Lab 1: 의존성 주입 생명주기 (Quiz 1)
Spring의 `@Service`는 싱글톤이지만, FastAPI의 `Depends`는 기본적으로 요청(Request) 스코프입니다.

### 실험 방법
1. 터미널 로그를 열어둡니다.
2. 브라우저나 curl로 아래 주소를 3번 호출합니다.
   `http://localhost:8000/study/lab1/scope`
3. 콘솔 로그에 `✅ MyService 인스턴스 생성됨!` 메시지가 몇 번 찍히는지 확인하세요.

### 결론
요청할 때마다 찍힌다면 **Request Scope** (Prototype)입니다.

---

## 🔬 Lab 2: N+1 문제 & Lazy Loading (Quiz 2)
Pydantic 모델로 변환될 때 Lazy Loading이 어떻게 동작하는지 봅니다.

### 실험 방법
1. 콘솔 로그를 주시합니다 (SQL 로그가 나옵니다).
2. User 1번을 조회합니다.
   `http://localhost:8000/study/lab2/lazy-loading/1`
3. 로그에 `SELECT ... FROM users ...` 외에 `SELECT ... FROM items ...` 쿼리가 추가로 나가는지 확인하세요.

### 결론
Pydantic이 `user.items` 필드를 읽으려 할 때, DB 세션이 아직 열려 있다면 **자동으로 추가 쿼리**가 실행됩니다. (N+1 발생)

---

## 🔬 Lab 3: Async Blocking (Quiz 3)
`async def` 안에서 동기 코드(`time.sleep`)를 썼을 때의 위험성을 확인합니다.

### 실험 방법
**시나리오 A: 안전한 동기 함수 (`def`)**
1. 탭 1에서 호출: `http://localhost:8000/study/lab3/sync-sleep` (5초 걸림)
2. 즉시 탭 2에서 다른 API 호출: `http://localhost:8000/` (바로 응답 옴)
-> **결과**: 서버가 멈추지 않음 (쓰레드풀 사용).

**시나리오 B: 위험한 비동기 함수 (`async def`)**
1. 탭 1에서 호출: `http://localhost:8000/study/lab3/async-sleep-blocking` (5초 걸림)
2. 즉시 탭 2에서 다른 API 호출: `http://localhost:8000/` (응답 안 옴! 5초 뒤에 옴)
-> **결과**: 이벤트 루프가 차단되어 **서버 전체가 멈춤**.

### 결론
`async def` 안에서는 절대 `time.sleep()`이나 무거운 계산, 동기식 DB 호출을 하면 안 됩니다.
