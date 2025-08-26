# ✅ 경량 베이스 이미지 사용
FROM python:3.11-slim AS base

# ✅ 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DASH_SERVE_LOCALLY=1 \
    PORT=8080

# ✅ 시스템 의존성 최소 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# ✅ 작업 디렉토리
WORKDIR /app

# ✅ 의존성 먼저 설치 → 캐시 활용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 애플리케이션 복사
COPY app.py .

# ✅ 포트 노출 (Cloud Run에서는 PORT 환경변수 자동 주입)
EXPOSE ${PORT}

# ✅ 헬스체크 (Cloud Run이 자체적으로 관리하지만, 로컬 테스트에도 유용)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -fs http://localhost:${PORT}/ || exit 1

# ✅ 프로덕션 서버 실행 (gunicorn)
ENV PORT=8080 DASH_SERVE_LOCALLY=1
CMD ["gunicorn", "app:server", "-b", "0.0.0.0:${PORT}", "--workers=2", "--threads=4", "--timeout=120"]
