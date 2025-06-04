# **EpiTrends** – Integracja systemów
## Informacje formalne

### Skład grupy:
- [SzymokArch](https://github.com/SzymokArch)
- [Netr0n07](https://github.com/Netr0n07)

### Wykorzystane technologie:
- Python 3.12
- Flask
- Pandas
- SQLAlchemy
- SQLite
- HTML, CSS, JavaScript
- Apache ECharts

## Opis projektu
Projekt EpiTrends analizuje dane z różnych źródeł (COVID-19, gospodarka, wydarzenia polityczne) i integruje je w jedną aplikację webową. Użytkownik może przeglądać dane i dostrzegać zależności między zjawiskami (np. wpływ szczepień na liczbę zgonów lub na poparcie rządu).

Przykładowe pytania, na które odpowiada aplikacja:
- Jak zmieniała się liczba szczepień w czasie?
- Czy wydarzenia polityczne miały wpływ na poparcie społeczne?
- Czy wzrost zachorowań koreluje ze spadkiem notowań giełdowych?

## Konfiguracja i uruchomienie
### Wymagania systemowe:
- Docker lub Python 3.12 z Flask, Pandas i SQLAlchemy
### Zaciągnięcie repozytorium
```bash
git clone https://github.com/SzymokArch/EpiTrends
cd EpiTrends
```

### Uruchomienie w Dockerze:
1. Zbuduj obraz:
```bash
docker build -t epitrends .
```
2. Uruchom kontener:
```bash
docker run -p 5000:5000 epitrends
```
### Alternatywnie (bez Dockera):

1. Utwórz wirtualne środowisko
```bash
virtualenv --python=python3.12 ~/venv/EpiTrends
source ~/venv/EpiTrends/bin/activate
```
2. Zainstaluj zależności
```bash
pip install -r requirements.txt
```
3. Uruchom aplikację:
```bash
python3.12 app.py
```
Aplikacja będzie dostępna pod adresem: [`http://localhost:5000`](http://localhost:5000)

## Wykorzystane źródła danych:
- [Dzienna i całkowita ilość śmierci na COVID-19](https://ourworldindata.org/grapher/total-daily-covid-deaths)
- [Całkowita ilość zaszczepień na COVID-19](https://ourworldindata.org/grapher/cumulative-covid-vaccinations)
- [Dzienna ilość zaszczepień na COVID-19](https://ourworldindata.org/grapher/daily-covid-19-vaccination-doses)
- [Poparcie rządu Polski](https://www.cbos.pl/PL/trendy/trendy.php?trend_parametr=stosunek_do_rzadu)
- [Wartości indeksu WIG20](https://stooq.pl/q/d/?f=20210101&t=20211130&s=wig20)
- Samodzielnie pozyskane dane na temat wydarzeń
