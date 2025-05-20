# Videreutvikling av Flask & Pygbag-prosjektet

Denne veiledningen er for deg som skal videreutvikle prosjektet. Her får du oversikt over hvordan filene henger sammen, funksjonaliteten, hvordan Pygbag er integrert (og begrensningene med det), samt forklaring på de mest komplekse delene av koden.

---

## Filstruktur og Sammenheng

```
AarsOppgaveKinda/
├── app.py                # Flask-backend, ruter og logikk for nettsiden
├── main.py               # Pygame-spill, kjøres via Pygbag
├── database.py           # Databasefunksjoner (brukere, bestillinger, poeng)
├── sql-kode.sql          # SQL for å sette opp databasen
├── pygame.toml           # Konfigurasjon for Pygbag
├── build/
│   └── web/              # Generert av Pygbag, inneholder spillfiler for web
├── templates/            # Flask-HTML-maler (Jinja2)
├── static/               # CSS og JS for Flask-sidene
└── requirements.txt      # Python-avhengigheter
```

- **app.py**: Hovedfil for Flask. Styrer ruter, brukerhåndtering, og kommunikasjon med databasen.
- **main.py**: Selve Pygame-spillet, som pakkes og kjøres i nettleseren via Pygbag.
- **database.py**: Funksjoner for å koble til og operere mot databasen (brukere, poeng, bestillinger).
- **templates/** og **static/**: Brukes av Flask for å vise nettsider og legge til stil/JS.
- **build/web/**: Genereres av Pygbag og inneholder alt som trengs for å kjøre spillet i nettleseren.

---

### .env
Dette er en **miljøvariabel-fil** som brukes til å lagre sensitiv informasjon og konfigurasjoner som ikke skal ligge åpent i koden eller på GitHub. Typiske verdier i .env-filen er:
- Database-navn, brukernavn og passord
- Hemmelige nøkler (f.eks. `SECRET_KEY` for Flask)
- Andre konfigurasjoner som kan variere mellom utvikling og produksjon

Eksempel:
```
DATABASE = "database_navn"
HOST = ip-adressen
USER = "brukernavn"
PASSWORD = "passord"
CHARSET = "utf8mb4"
SECRET_KEY = "hemlig_nøkkel"
```
**Viktig:** Denne filen skal aldri pushes til GitHub, derfor står den i .gitignore.

---

### .gitignore
Dette er en fil som forteller Git hvilke filer og mapper som **ikke** skal inkluderes i versjonskontrollen (GitHub). Typiske ting man ignorerer er:
- .env-filer (sensitive data)
- Midlertidige filer, cache, og byggemapper
- Virtuelle miljøer (f.eks. `venv/`)

Eksempel:
```
.env
venv/
__pycache__/
```
Dette beskytter sensitiv informasjon og holder repoet ryddig.

---

### pygame.toml
Dette er en **konfigurasjonsfil for Pygbag**. Den brukes til å fortelle Pygbag hvilke filer som skal inkluderes når spillet pakkes for web, og kan også inneholde metadata om prosjektet.

Eksempel:
```toml
[project]
name = "main"

[files]
"pygameBilder/kaktus.png" = "pygameBilder/kaktus.png"
```
Her sier du at bildet `kaktus.png` skal pakkes med i web-versjonen av spillet.

---

**Oppsummert:**  
- .env = sensitiv konfigurasjon, brukes av koden, ikke i Git
- .gitignore = forteller Git hva som skal ignoreres
- pygame.toml = styrer hva Pygbag tar med når det bygger web-versjonen av spillet

Dette gjør prosjektet sikrere, ryddigere og enklere å bygge for web!
---

## Funksjonalitet

- **Brukerregistrering og innlogging**: Brukere kan registrere seg og logge inn. Admin-brukere har tilgang til ekstra funksjoner.
- **Bokbestillinger**: Brukere kan bestille bøker og se sine bestillinger.
- **Poengsystem**: Poeng fra spillet kan (teoretisk) lagres, men dette fungerer ikke optimalt pga. Pygbag/WebAssembly-begrensninger.
- **Spill**: Et Pygame-spill kjøres i nettleseren via Pygbag.

---

## Hvordan Pygbag Fungerer (og Begrensninger)

**Pygbag** gjør det mulig å kjøre Pygame-spill i nettleseren ved å konvertere Python-koden til WebAssembly. Når du kjører `pygbag main.py`, genereres en web-app i `build/web/`-mappen.

**Begrensning:**  
Pygbag kjører spillet i nettleseren isolert fra Flask-serveren (backend). Dette gjør det vanskelig å sende data (som poeng) direkte fra spillet til Flask/databasen, fordi WebAssembly-miljøet ikke har direkte tilgang til serverens Python-funksjoner eller database. Kommunikasjon må eventuelt skje via HTTP-forespørsler (API), men dette krever ekstra arbeid og tilpasning i både spillkoden og Flask.

**Konsekvens:**  
Poeng og annen data fra spillet blir ikke automatisk lagret i databasen. For å få dette til å fungere må du lage et REST-API i Flask og sende data fra spillet med JavaScript (fetch/XHR).

---

## Komplekse Deler av Koden

### 1. **Session-håndtering i Flask (`app.py`)**
Flask bruker `session`-objektet for å holde styr på innloggede brukere og deres roller. Dette gjør det mulig å vise ulike sider/funksjoner basert på om brukeren er admin eller vanlig bruker.

Eksempel:
```python
@app.context_processor
def current_user():
    return dict(username=session.get('username'), role=session.get('role'), ...)
```

### 2. **Databasekobling og -operasjoner (`database.py`)**
Funksjonene for å koble til og operere mot databasen bruker miljøvariabler for sikkerhet. Det er egne funksjoner for å hente brukere, lagre bestillinger, og (teoretisk) lagre poeng.

Eksempel:
```python
def opprett_bruker(navn, etternavn, email, passord, role="user"):
    ...
    cursor.execute(sql, (navn, etternavn, email, passord_hash, role))
    ...
```

### 3. **Spillintegrasjon (`main.py` og Pygbag)**
Spillet i `main.py` er laget med Pygame og kjøres i nettleseren via Pygbag. All logikk for bevegelse, poeng, og kollisjoner ligger her. Siden det kjøres i nettleseren, er det isolert fra Flask-backend.

Eksempel på spill-løkke:
```python
async def main():
    while True:
        ...
        all_sprites.update()
        all_sprites.draw(screen)
        ...
        pygame.display.flip()
        await asyncio.sleep(0)
```

### 4. **Templates og Arv**
HTML-filene i `templates/` bruker Jinja2-arv (`{% extends "navbar.html" %}`) for å gjenbruke felles elementer som navigasjonsmeny. Dette gjør det enklere å endre utseendet på hele siden fra ett sted.

---




## Utviklingsmiljø og Kjøring

- **Virtuelt miljø:**  
  Opprett gjerne et virtuelt miljø for å holde avhengigheter adskilt:
  ```bash
  python -m venv venv
  source venv\Scripts\activate
  pip install -r requirements.txt
  ```

## Testing og Feilhåndtering

- **Testing av spill:**  
  Skriv /debug på slutten av url-en til spillet for å kjøre en debug versjon av spillet.
- **Debugging:**  
  Flask sin debug-modus gir gode feilmeldinger.  
  Sjekk også nettleserens konsoll for JavaScript-feil.

---

## Avhengigheter og Oppdatering

- Legg til nye Python-pakker med:
  ```bash
  pip install pakkenavn
  pip freeze > requirements.txt
  ```
- Husk å holde requirements.txt oppdatert.

---

## Sikkerhet

- Ikke legg sensitive data i kode eller repo (bruk .env-fil).
- Bruk sikre passord og vurder HTTPS hvis prosjektet skal på nett.
- Valider og sjekk all input fra brukere.

---


## Tips for Videreutvikling

- **Forbedre kommunikasjon mellom spill og backend:**  
  Hvis du ønsker å lagre poeng fra spillet, må du implementere et API-endepunkt i Flask og sende data fra spillet med JavaScript (fetch/XHR).
- **Utvid funksjonalitet i Flask:**  
  Legg til flere ruter og templates for nye sider eller funksjoner.
- **Forbedre spillopplevelsen:**  
  Legg til flere nivåer, grafikk eller lyd i main.py.
- **Sikkerhet:**  
  Sørg for at brukerdata og innlogging håndteres sikkert, spesielt hvis prosjektet skal på nett.




