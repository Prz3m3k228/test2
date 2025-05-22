
# Luxury Car Rental API

A REST API for managing a luxury car rental service, created as part of a student term project.

## Wymagania

- Python 3.8+ (zalecana wersja: 3.10 lub wyższa)
- PostgreSQL (lub dowolna baza danych kompatybilna z SQLAlchemy)
- `pip` (menedżer pakietów dla Pythona)

## Instalacja

1. **Sklonuj repozytorium**:

   Skopiuj projekt na swoje lokalne środowisko:

   ```bash
   git clone https://github.com/yourusername/luxury-car-rental-api.git
   cd luxury-car-rental-api
   ```

2. **Utwórz i aktywuj wirtualne środowisko** (opcjonalne, ale zalecane):

   - Na Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - Na macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Zainstaluj wymagane zależności**:

   Użyj pliku `requirements.txt` do zainstalowania wszystkich zależności:

   ```bash
   pip install -r requirements.txt
   ```

4. **Skonfiguruj bazę danych**:

   Upewnij się, że masz zainstalowaną i uruchomioną bazę danych PostgreSQL. W pliku `database.py` znajduje się domyślny adres połączenia do bazy danych. Możesz go zmienić, jeśli Twoja baza jest na innym hoście lub ma inne dane logowania:

   ```python
   DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/rental_cars"
   ```

   W razie potrzeby stwórz bazę danych `rental_cars` w PostgreSQL:

   ```bash
   psql -U postgres
   CREATE DATABASE rental_cars;
   ```

## Uruchomienie aplikacji

1. **Uruchom serwer**:

   Aby uruchomić aplikację FastAPI, użyj serwera ASGI, np. `uvicorn`:

   ```bash
   uvicorn main:app --reload
   ```

   Parametr `--reload` powoduje automatyczne przeładowanie aplikacji przy każdej zmianie w kodzie, co jest przydatne podczas pracy nad projektem.

2. **Dostęp do API**:

   Po uruchomieniu aplikacji, API będzie dostępne pod adresem: `http://127.0.0.1:8000`. Możesz teraz korzystać z interfejsu API, np. odwiedzić `http://127.0.0.1:8000/docs`, aby uzyskać dostęp do automatycznie generowanej dokumentacji API (dzięki FastAPI i Swagger).