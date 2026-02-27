import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window, to_date
from pyspark.sql.window import Window

# Инициализация с драйвером
spark = SparkSession.builder \
    .appName("FinanceETL") \
    .config("spark.jars", "/app/postgresql-42.7.5.jar") \
    .config("spark.driver.extraClassPath", "/app/postgresql-42.7.5.jar") \
    .getOrCreate()

# Настраиваю БДшку (из docker-compose)
DB_URL = "jdbc:postgresql://postgres:5432/finance_dw"
DB_PROPS = {
    "user": os.getenv("POSTGRES_USER", "VladislavDubinkin"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "driver": "org.postgresql.Driver"
}
def process_ticker(ticker_file):
    print(f"⚡ Processing {ticker_file}...")
    
    # Extract (E)
    df = spark.read.csv(f"/app/data/raw/{ticker_file}", header=True, inferSchema=True)
    
    # Transform (T)
    df_clean = df.withColumn("Date", to_date(col("Date")))
    
    # Здесь я нахожу 7-дневное скользящее среднее (aka Moving Average)
    w = Window.orderBy("Date").rowsBetween(-6, 0)
    df_transformed = df_clean.withColumn("MA_7", avg("Close").over(w))
    
    final_df = df_transformed.select("Date", "ticker", "Close", "MA_7")

    # Load (L)
    final_df.write.jdbc(url=DB_URL, table="fact_stocks", mode="append", properties=DB_PROPS)
    print(f"Успешно записан {ticker_file} в ДБ")

if __name__ == "__main__":
    target_files = ["nvda.csv", "aapl.csv", "tsla.csv", "btc-usd.csv"]
    
    for filename in target_files:
        try:
            process_ticker(filename)
        except Exception as e:
            print(f"Ошибка обработки {filename}: {e}")
    
    spark.stop()
