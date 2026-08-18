# Build the Command Desk with a pinned major Node runtime.
FROM node:24-bookworm-slim AS frontend-build
WORKDIR /build/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm run build

# Serve the compiled interface and API from one minimal Python runtime.
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    SLATEGUARD_STATIC_DIR=/app/frontend/dist
WORKDIR /app
COPY requirements-app.txt requirements-sprint0.txt ./
RUN pip install --no-cache-dir -r requirements-app.txt -r requirements-sprint0.txt
COPY backend/ ./backend/
# Keep the self-authored seed and evaluation fixtures available to the container
# test stage; they are not exposed by the running HTTP service.
COPY clickhouse/ ./clickhouse/
COPY --from=frontend-build /build/frontend/dist ./frontend/dist/
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
