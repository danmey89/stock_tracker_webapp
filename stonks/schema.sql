DROP TABLE IF EXISTS stock_data;


CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT UNIQUE NOT NULL,
    shortName TEXT NOT NULL,
    currency TEXT NOT NULL,
    regularMarketPrice FLOAT,
    postMarketPrice FLOAT,
    postMarketChange FLOAT,
    regularMarketChange FLOAT,
    regularMarketDayHigh FLOAT,
    regularMarketDayRange FLOAT,
    regularMarketDayLow FLOAT,
    regularMarketVolume FLOAT,
    regularMarketPreviousClose FLOAT,
    regularMarketOpen  FLOAT,
    bid FLOAT,
    ask FLOAT,
    averageDailyVolume3Month FLOAT,
    averageDailyVolume10Day FLOAT,
    fiftyDayAverage FLOAT,
    fiftyDayAverageChange FLOAT,
    fiftyDayAverageChangePercent  FLOAT,
    marketCap FLOAT,
    averageAnalystRating TEXT
);