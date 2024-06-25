DROP TABLE IF EXISTS quote;
DROP TABLE IF EXISTS history;

CREATE TABLE quote (
    symbol TEXT PRIMARY KEY NOT NULL,
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

CREATE TABLE history (
    idate TIMESTAMP PRIMARY KEY NOT NULL,
    AAPL INT,
    GOOGL INT,
    META INT,
    NFLX INT,
    NVDA INT
);