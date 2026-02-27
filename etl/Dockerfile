# Используем Python 3.11 (Debian Bookworm)
FROM python:3.11

# 1. Установка Java (Обязательно для PySpark)
# Обновляем пакеты и ставим OpenJDK 17
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

WORKDIR /app

# 2. Установка библиотек
COPY requirements.txt .
# Увеличиваем таймаут, так как PySpark 4.0 весит >300MB
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY . .
CMD ["tail", "-f", "/dev/null"]
