FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependências de sistema mínimas (útil caso boto3 precise compilar C)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas os requirements inicialmente para aproveitar cache
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Agora copia o restante da aplicação
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
