FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Instala dependências do sistema (vídeo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia só os requirements primeiro (melhor uso do cache Docker)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Depois copia o restante da aplicação
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["python", "-m", "app.main"]
