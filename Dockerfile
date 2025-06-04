# Wybór obrazu bazowego z Pythona
FROM python:3.12-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików projektu
COPY . .

# Instalacja zależności
COPY requirements.txt .
RUN pip install -r requirements.txt

# Tworzenie bazy danych podczas budowy obrazu
RUN python JSONToDatabase.py

# Eksponowanie portu
EXPOSE 5000

# Komenda uruchamiająca aplikację
CMD ["python", "app.py"]
