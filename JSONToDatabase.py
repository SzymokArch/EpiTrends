import pandas as pd
from sqlalchemy import create_engine

df = pd.read_json("integrated_data.json")

# Konwersja kolumny 'date' do typu datetime.date (bez czasu)
df['date'] = pd.to_datetime(df['date']).dt.date

engine = create_engine("sqlite:///covid_data.db")

df.to_sql("daily_data", con=engine, if_exists="replace", index=False)

print("✅ Dane zostały zapisane do bazy danych 'covid_data.db' w tabeli 'daily_data'.")
