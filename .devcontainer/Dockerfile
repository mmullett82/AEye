FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt || true
