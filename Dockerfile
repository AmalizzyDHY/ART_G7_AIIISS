FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LLM_PROVIDER=mock \
    SCENARIO_ID=g07 \
    DB_PATH=/data/analyses.db \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir --no-deps .

COPY scenarios/ ./scenarios/
COPY ui/ ./ui/

RUN useradd --create-home --uid 10001 appuser \
 && mkdir -p /data && chown appuser:appuser /data
USER appuser

EXPOSE 8000 8501
# Default command starts the API; the UI container overrides it.
CMD ["python", "-m", "uvicorn", "ticket_app.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
