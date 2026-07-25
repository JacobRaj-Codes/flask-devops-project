# ---- Build stage ----
FROM python:3.12-slim AS builder

WORKDIR /install

COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

# ---- Final stage ----
FROM python:3.12-slim

# Run as non-root user (security best practice, also improves Trivy results)
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

COPY --from=builder /install/deps /usr/local
COPY app/ .

USER app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
