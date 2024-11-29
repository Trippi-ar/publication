FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libnspr4 \
    libglib2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libx11-xcb1 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libxcb1 \
    libexpat1 \
    libsm6 \
    libxext6 \
    libcairo2 \
    libglib2.0-bin \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright && playwright install

COPY . .

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
