FROM python:3.12-slim

# Evita prompts do apt
ENV DEBIAN_FRONTEND=noninteractive

# Cria diretório da aplicação
WORKDIR /app

# Instala dependências de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia somente requirements.txt primeiro (melhora cache)
COPY requirements.txt .

# Instala pacotes Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Agora copia o restante da aplicação
COPY . .

# Define o PYTHONPATH para que os imports funcionem bem
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Porta exposta para consistência
EXPOSE 8004

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
