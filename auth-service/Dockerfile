FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
