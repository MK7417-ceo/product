# Build context for this Dockerfile is part-1-core/ (see render.yaml).
# Stage 1: build the React frontend.
# NOTE: uses `npx vite build`, not `npm run build`, because the repo's
# build script also runs `tsc -b`, which currently fails on 50
# pre-existing type errors (tsc cleanup is a separate follow-up).
FROM node:20-slim AS frontend-build
WORKDIR /src/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npx vite build

# Stage 2: Python backend + built frontend (single origin: the backend
# serves frontend/dist itself, so no CORS/proxy setup is needed).
FROM python:3.12-slim
WORKDIR /srv/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY --from=frontend-build /src/frontend/dist ./frontend/dist
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
