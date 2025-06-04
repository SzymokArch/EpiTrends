import pandas as pd
from datetime import datetime, timedelta

# Zakres dat
start_date = "2019-01-01"
end_date = "2023-12-31"
date_range = pd.date_range(start=start_date, end=end_date)

# 1. Zgony COVID
deaths = pd.read_csv("total-daily-covid-deaths.csv")
deaths["Day"] = pd.to_datetime(deaths["Day"])
deaths = deaths[deaths["Day"].between(start_date, end_date)]
deaths = deaths[["Day", "Daily new confirmed deaths due to COVID-19"]].rename(
    columns={"Day": "date", "Daily new confirmed deaths due to COVID-19": "covid_deaths"}
)

# 2. Szczepienia skumulowane
vacc = pd.read_csv("cumulative-covid-vaccinations.csv")
vacc["Day"] = pd.to_datetime(vacc["Day"])
vacc = vacc[vacc["Day"].between(start_date, end_date)]
vacc = vacc[["Day", "COVID-19 doses (cumulative)"]].rename(
    columns={"Day": "date", "COVID-19 doses (cumulative)": "vaccinations"}
)

# 2b. Dzienna średnia szczepień (7-dniowa)
daily_vacc = pd.read_csv("daily-covid-19-vaccination-doses.csv")
daily_vacc["Day"] = pd.to_datetime(daily_vacc["Day"])
daily_vacc = daily_vacc[daily_vacc["Day"].between(start_date, end_date)]
daily_vacc = daily_vacc[["Day", "COVID-19 doses (daily, 7-day average)"]].rename(
    columns={"Day": "date", "COVID-19 doses (daily, 7-day average)": "daily_vaccinations"}
)

# 3. WIG20
wig = pd.read_csv("wig20_d.csv", sep=",")
wig["Data"] = pd.to_datetime(wig["Data"], format="%Y-%m-%d")
wig = wig[wig["Data"].between(start_date, end_date)]
wig = wig[["Data", "Zamkniecie"]].rename(columns={"Data": "date", "Zamkniecie": "wig20"})

# 4. Poparcie rządu (miesięczne -> rozciągnięte na dni)
support = pd.read_csv("poparcie.csv", sep=";")
month_map = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6,
    'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12
}
dates = []
for m in support["XLSMiesiac"]:
    parts = m.strip().split()
    if len(parts) == 2:
        month = month_map.get(parts[0])
        year = int(parts[1])
        if month and 2019 <= year <= 2023:
            dates.append(datetime(year, month, 1))
        else:
            dates.append(None)
    else:
        dates.append(None)

support["date"] = dates
support = support.dropna(subset=["date"])
support["government_support"] = pd.to_numeric(support["Zwolennicy"], errors="coerce")
support = support[["date", "government_support"]].sort_values("date").reset_index(drop=True)

support_daily = []
for i in range(len(support)):
    start = support.loc[i, "date"].date()
    if i + 1 < len(support):
        end = (support.loc[i + 1, "date"] - timedelta(days=1)).date()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    for d in pd.date_range(start=start, end=end):
        support_daily.append({"date": d, "government_support": support.loc[i, "government_support"]})

support = pd.DataFrame(support_daily)

# 5. Scalanie danych
df = pd.DataFrame({"date": date_range})
df = df.merge(deaths, on="date", how="left")
df = df.merge(vacc, on="date", how="left")
df = df.merge(daily_vacc, on="date", how="left")          # <-- dodano dzienne szczepienia
df = df.merge(wig, on="date", how="left")
df = df.merge(support, on="date", how="left")

# Wypełnienie brakujących wartości forward fill (oprócz covid_deaths, które mogą być 0)
df[["vaccinations", "daily_vaccinations", "wig20", "government_support"]] = \
    df[["vaccinations", "daily_vaccinations", "wig20", "government_support"]].fillna(method="ffill")

# Zapis do JSON
df["date"] = df["date"].dt.strftime("%Y-%m-%d")
df = df.sort_values("date")
df.to_json("integrated_data.json", orient="records", indent=2)

print("✅ Plik 'integrated_data.json' został wygenerowany z dziennymi szczepieniami.")
