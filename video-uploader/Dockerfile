FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Instala bibliotecas básicas do sistema (caso precise compilar algo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia só os requirements primeiro para aproveitar o cache
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
