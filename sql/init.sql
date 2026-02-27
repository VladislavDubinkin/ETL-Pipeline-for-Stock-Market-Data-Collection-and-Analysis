CREATE TABLE IF NOT EXISTS fact_stocks (
    date        DATE NOT NULL,
    ticker      VARCHAR(10) NOT NULL,
    close       NUMERIC(12, 4),
    ma_7        NUMERIC(12, 4),
    created_at  TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (date, ticker)
);