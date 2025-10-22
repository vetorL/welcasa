# ---- Stage 1: Build frontend ----
FROM node:22-alpine AS web-build
WORKDIR /web
# if you use pnpm/yarn, swap the next lines accordingly
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

# ---- Stage 2: API runtime + static files ----
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps (keep minimal, exactly as your README)
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy backend code
COPY backend/app.py ./app.py

# Copy built frontend into ./static (served by FastAPI)
COPY --from=web-build /web/dist ./static

# SQLite data directory (mount a volume here for persistence)
RUN mkdir -p /data
ENV DATABASE_PATH=/data/properties.db

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://localhost:8000/ || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
