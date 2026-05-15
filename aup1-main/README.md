# Algoritmi u primjeni

Ovaj projekt je jednostavna Flask aplikacija povezana na MySQL bazu preko `Flask-SQLAlchemy` i `Flask-Migrate`.

Projekt trenutno koristi:
- `Flask`
- `Flask-SQLAlchemy`
- `Flask-Migrate`
- `PyMySQL`

Baza podataka koja se koristi u projektu zove se `aup1`.

## 1. XAMPP i baza podataka

Prvo treba pokrenuti XAMPP.

1. Otvoriti XAMPP Control Panel.
2. Pokrenuti `Apache`.
3. Pokrenuti `MySQL`.

`Apache` nam treba zbog `phpMyAdmin`, a `MySQL` zbog same baze podataka.

Nakon toga otvoriti:

```text
http://localhost/phpmyadmin
```

Ako traži prijavu, zadani podaci su obično:

- korisničko ime: `root`
- lozinka: nema lozinke

U `phpMyAdmin` treba napraviti novu praznu bazu podataka:

```text
aup1
```

Nije potrebno ručno praviti tablice. Tablice će se napraviti kroz migracije.

## 2. Virtualno okruženje kroz PyCharm

Preporuka je da se virtualno okruženje napravi kroz PyCharm.

Koraci u PyCharmu:

1. Otvoriti projekt.
2. Otići na `Settings` / `Preferences`.
3. Otvoriti `Project: ... > Python Interpreter`.
4. Odabrati `Add Interpreter`.
5. Odabrati `Virtualenv Environment`.
6. Napraviti novo okruženje unutar projekta kao `.venv`.

Kad je interpreter pravilno postavljen, PyCharm će koristiti to virtualno okruženje za pokretanje projekta i instalaciju paketa.

## 3. Ručno kreiranje virtualnog okruženja

Ako se `.venv` ne napravi kroz PyCharm, može ručno kroz terminal.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 4. Instalacija paketa

Nakon aktivacije virtualnog okruženja instaliraju se paketi:

```bash
python -m pip install -r requirements.txt
```

Ako treba ručno instalirati pakete:

```bash
python -m pip install flask flask-sqlalchemy flask-migrate pymysql
```

Ako nakon instalacije želiš osvježiti `requirements.txt`:

```bash
python -m pip freeze > requirements.txt
```

## 5. Važna napomena prije `flask db` naredbi

Da bi `flask db init`, `flask db migrate` i `flask db upgrade` radili ispravno, preporuka je da se u `app.py` pokretanje servera stavi na kraj datoteke ovako:

```python
if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

Ako `app.run(...)` stoji samostalno bez ovog uvjeta, `flask` naredbe mogu pokušati odmah pokrenuti server umjesto migracija.

## 6. Flask migracije

Pošto je `migrations` folder obrisan, treba ga napraviti ponovno.

Sve naredbe pokretati iz root foldera projekta.

### 6.1. Inicijalizacija migracija

```bash
flask db init
```

Ova naredba ponovno stvara folder `migrations`.

### 6.2. Kreiranje prve migracije

```bash
flask db migrate -m "pocetna migracija"
```

Ova naredba čita modele iz `models.py` i priprema skriptu za izradu tablica.

### 6.3. Primjena migracija na bazu

```bash
flask db upgrade
```

Nakon ove naredbe tablice će biti napravljene u bazi `aup1`.

## 7. Kada promijeniš modele

Ako kasnije dodaš novu tablicu ili promijeniš postojeći model, treba ponovno pokrenuti:

```bash
flask db migrate -m "opis promjene"
flask db upgrade
```

Primjeri:

```bash
flask db migrate -m "napravljena tablica ucionice"
flask db upgrade
```

```bash
flask db migrate -m "dodani termini nastave"
flask db upgrade
```

## 8. Pokretanje aplikacije

Aplikacija se pokreće naredbom:

```bash
python app.py
```

U ovom projektu server se pokreće na portu:

```text
5000
```

Pa se aplikaciji pristupa preko:

```text
http://127.0.0.1:5000
```

## 9. Kratki redoslijed rada

Ako krećeš od početka, redoslijed je:

1. Pokrenuti XAMPP.
2. Uključiti `Apache` i `MySQL`.
3. U `phpMyAdmin` napraviti bazu `aup1`.
4. Napraviti `.venv` kroz PyCharm ili ručno.
5. Aktivirati virtualno okruženje.
6. Instalirati pakete iz `requirements.txt`.
7. Pokrenuti `flask db init`.
8. Pokrenuti `flask db migrate -m "pocetna migracija"`.
9. Pokrenuti `flask db upgrade`.
10. Pokrenuti aplikaciju s `python app.py`.

## 10. Korisne napomene

- `.venv` se ne commita na Git.
- `requirements.txt` služi za dijeljenje paketa potrebnih za projekt.
- `migrations` folder se commita na Git jer sadrži povijest promjena baze.
- Ako je obrisan `migrations` folder, `flask db init` ga pravi ponovno.
- Baza mora postojati prije pokretanja migracija, zato prvo treba napraviti `aup1` u `phpMyAdmin`.
- Ako `flask db ...` ne radi zato što Flask ne zna koju aplikaciju treba koristiti, tada koristi eksplicitnu varijantu: `flask --app app db init`, `flask --app app db migrate` i `flask --app app db upgrade`.
