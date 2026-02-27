# 📈 ETL Pipeline for Stock Market Data Collection and Analysis

В этом проекте я постарался рарзработать и имплементировать автоматизированный ETL-пайплайн для сбора, обработки и хранения биржевых данных с оркестрацией через Apache Airflow. Приятного прочтения!

---

## Архитектура:

```
Yahoo Finance API
       │
       ▼
  [extract.py]          ← Python + yfinance
       │ CSV
       ▼
  data/raw/             ← Landing Zone
       │
       ▼
  [transform.py]        ← PySpark 4.0 (оконные функции, MA_7)
       │ JDBC
       ▼
  PostgreSQL            ← finance_dw.fact_stocks
       │
  [Apache Airflow]      ← Оркестрация (расписание + зависимости тасков)
```
![alt text]([https://example.com/my-image.svg](https://imgur.com/a/pzKS6JS))


> Полная архитектурная схема: `docs/architecture.drawio`

---

## Стэк:

| Этап: | Стэк: |
|---|---|
| Extract | Python 3.11, yfinance |
| Transform | PySpark 4.0, оконные функции |
| Load | PostgreSQL 13, JDBC |
| Orchestration | Apache Airflow 2.9.0 |
| Infrastructure | Docker, Docker Compose |

---

## Структура проекта:

```
finance_etl/
├── dags/
│   └── finance_etl_dag.py     # Airflow DAG: extract >> transform
├── etl/
│   ├── Dockerfile
│   ├── extract.py             # Загрузка данных через yfinance
│   ├── transform.py           # PySpark: очистка, анализ, загрузка в БД
│   ├── requirements.txt
│   └── postgresql-42.7.5.jar  # JDBC драйвер
├── data/
│   └── raw/                  
├── .env.example               # Шаблон переменных окружения
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Быстрый старт:

### 1. Клон репозитория:

```bash
git clone https://github.com/ВАШ_USERNAME/finance-etl.git
cd finance-etl
```

### 2. Настройка переменные окружения:

```bash
cp .env.example .env
# Отредактировать .env: указать свои POSTGRES_USER и POSTGRES_PASSWORD
```

### 3. Создание папки для DAGов:

```bash
mkdir dags
```

### 4. Запуск все сервисы:

```bash
docker-compose up --build -d
```

### 5. Проверка (что всё запустилось):

```bash
docker-compose ps
```

### 6. Заход в Airflow UI по ссылке:

```
http://localhost:8080
Логин: admin
Пароль: admin
```

### 7. Запуск самого пайплайна:

В Airflow UI найти DAG `finance_etl` → включить тумблер → нажать ▶ (Trigger DAG).

### 8. Проверка данных в PostgreSQL:

```bash
docker exec finance_warehouse psql -U ВАШ_USERNAME -d finance_dw -c "SELECT ticker, COUNT(*) as rows, MIN(\"Date\") as from_date, MAX(\"Date\") as to_date FROM fact_stocks GROUP BY ticker;"
```

---

## Итог:

После успешного запуска в таблице будут данные:


```
 ticker  | rows | from_date  |  to_date
---------+------+------------+------------
 AAPL    |  789 | 2024-01-01 | 2026-02-27
 BTC-USD |  789 | 2024-01-01 | 2026-02-27
 NVDA    |  789 | 2024-01-01 | 2026-02-27
 TSLA    |  789 | 2024-01-01 | 2026-02-27
```

Схема таблички:

| Колонка | Тип | Описание |
|---|---|---|
| Date | DATE | Дата торгов |
| ticker | VARCHAR | Тикер инструмента |
| Close | NUMERIC | Цена закрытия |
| MA_7 | NUMERIC | 7-дневное скользящее среднее |

---

## 🔄 Как работает DAG

```
extract  ──►  transform
```

- **extract** — запускает файл `extract.py`, он скачивает данные с Yahoo Finance для 4 компаний (AAPL, NVDA, TSLA, BTC-USD) и сохраняет CSV в `data/raw/`.
- **transform** — запускает `transform.py`, он в свою очередь читает CSV через PySpark, считает скользящую среднюю через оконные функции, загружает результат в PostgreSQL уже через JDBC.

Расписание: каждый будний день в 06:00 UTC (`0 6 * * 1-5`)

---

## 🖼️ Скриншоты

### Airflow DAG — успешный запуск
> *(скриншот)*

### Данные в PostgreSQL
> *(скриншот)*

### MA_7 для NVDA
> *(скриншот)*

### Docker Desktop
> *(скриншот)*

---

## 🔧 Сервисы Docker Compose

| Сервис | Образ | Описание |
|---|---|---|
| postgres | postgres:13 | Хранилище биржевых данных |
| etl-worker | finance_etl-etl-worker | Python + PySpark воркер |
| airflow-db | postgres:15 | Метаданные Airflow |
| airflow-init | apache/airflow:2.9.0 | Инициализация (запускается один раз) |
| airflow-webserver | apache/airflow:2.9.0 | UI на localhost:8080 |
| airflow-scheduler | apache/airflow:2.9.0 | Планировщик задач |

---
