import yfinance as yf
import pandas as pd
import os

SYMBOLS = ["NVDA", "AAPL", "TSLA", "BTC-USD"] # Всякие тикеры, решил взять Nvida, Apple, Tesla и биткоин из интереса
START_DATE = "2024-01-01"
OUTPUT_DIR = "/app/data/raw"

def extract_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Начинаем загрузку данных для: {SYMBOLS}")
    
    # Качаем
    data = yf.download(SYMBOLS, start=START_DATE, group_by='ticker', auto_adjust=True)
    
    # Сохраняем (Parquet был бы лучше, но CSV будет понагляднее)
    for ticker in SYMBOLS:
        df = data[ticker].copy()
        df['ticker'] = ticker
        df.reset_index(inplace=True)
        
        filename = f"{ticker.lower().replace('.', '_')}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        df.to_csv(filepath, index=False)
        print(f"Сохранено: {filepath} ({len(df)} строк)")

if __name__ == "__main__":
    extract_data()
