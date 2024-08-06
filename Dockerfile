# Use uma imagem base do Ubuntu
FROM ubuntu:20.04

# Defina o argumento para desativar as perguntas interativas durante a instalação
ARG DEBIAN_FRONTEND=noninteractive

# Atualize o sistema e instale dependências básicas, incluindo python3-venv
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    vim \
    sudo \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    nmap \
    net-tools \
    psmisc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crie e ative o ambiente virtual
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instale dependências do Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copie a aplicação Python para o container
COPY . /app

# Defina o diretório de trabalho
WORKDIR /app

# Exponha a porta necessária para a aplicação
EXPOSE 5000

# Comando de inicialização padrão
CMD ["python", "app.py"]
