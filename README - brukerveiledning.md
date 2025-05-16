# Flask og Pygbag Webapplikasjon - Brukerveiledning

Dette prosjektet er en Flask-basert webapplikasjon som inkluderer funksjonalitet for brukerregistrering, innlogging, bokbestillinger, poengsystem og et Pygbag-spill som kjører i nettleseren.

Dette er en nettside med bare funksjonalitet og ikke noe praksis bruk

## Innhold

- [Oversikt](#oversikt)
- [Krav](#krav)
- [Installasjon](#installasjon)
- [Oppsett](#oppsett)
- [Bruk](#bruk)
- [Funksjonalitet](#funksjonalitet)
- [Filstruktur](#filstruktur)
- [Feilsøking](#feilsøking)
- [Kontakt](#kontakt)

---

## Oversikt

Applikasjonen består av flere komponenter:
- **Flask**: Backend for å håndtere ruter, brukerdata og databaseoperasjoner.
- **Pygbag**: Spillmotor som kjører et spill i nettleseren.
- **MySQL/MariaDB**: Database for å lagre brukere, poeng(funker ikke pga pygbag sitt bruk av WebAssembly) og bestillinger.
- **HTML/CSS/JavaScript**: Frontend for å vise nettsider og interaktive elementer.

---

## Krav

For å kjøre prosjektet trenger du:
- **Python 3.10 eller nyere**
- **Pip** (Python-pakkebehandler)
- **MySQL/MariaDB**
- **Pygbag** (for å bygge og kjøre spillet)
- En moderne nettleser som støtter HTML5 og JavaScript.

---

## Installasjon

1. **Klon prosjektet:**
   ```bash
   Åpne et cmd vindu og bruk cd til å navigere til mappen du vil klone prosjektet til og skriv:
   "git clone git@github.com:Chewbacca176/-rs-oppgave-kinda.git"
   og skriv "cd Aaroppgavekinda" for å gå inn i prosjekt mappen 
   ```

2. **Installer nødvendige Python-pakker:**
   ```bash
   pip install -r requirements.txt
   ```



3. **Sett opp MySQL-databasen:**
   - Sørg for at brukernavn og passord i `database.py` under `connect_to_mariadb()` og `connect_to_db()` samsvarer med din MySQL-konfigurasjon.
   - Hvis ikke så må du enten bytte brukernavn og passord i documentet eller lage en ny bruker inni mariadb 
   - Eller hvis du ikke har brukt mariadb før så må du laste det ned via nette https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.7.2&os=windows&cpu=x86_64&pkg=msi&mirror=dotsrc.
   - Etter du har lastet ned mariadb så kan du velge mellom å bruke "root" brukern eller lage en ny bruker. Hvis du vil bruke "root" brukern så bytter du innloggings informasjonen i `database.py` med brukernavn "root" og passordet blir passordet på pc-en din. Hvis du ikke vil lage en ny bruker så åpner du et cmd vindu og skriv inn: `cd /"program files"/"MariaDB 11.6"/bin` så skriver du `mariadb -u root -p`
   så skriver du inn passordet på pc-en din, da har du fått tilgang til mariadb
   - For å lage en bruker så skrier du `CREATE USER 'bruker'@'%' IDENTIFIED BY 'passord';` deretter `GRANT ALL PRIVILEGES ON *.* TO 'bruker'@'%' IDENTIFIED BY 'passord';`, så bytter du innloggings informasjonen i `database.py` med den informasjonen du lagde brukeren med.



---

## Oppsett

1. **Bygg Pygbag-spillet:**
   Naviger til prosjektmappen og kjør:
   ```bash
   pygbag --host 3001 main.py
   ```
   Dette vil starte pygbag serveren som kjører spillet.

2. **Start Flask-applikasjonen:**
   Kjør følgende kommando:
   ```bash
   python app.py
   ```
   Flask-applikasjonen vil kjøre på `http://localhost:3000`.


---

## Bruk

### Navigasjon
- **Hjemmeside:** `http://localhost:3000/`
- **Spill:** `http://localhost:3000/pygameSpill`
- **Logg inn:** `http://localhost:3000/logginn`
- **Registrer:** `http://localhost:3000/registrer`
- **Bokbestillinger:** `http://localhost:3000/bestillinger`
- **Se bestillinger:** `http://localhost:3000/sebestillinger`
- **Global score:** `http://localhost:3000/global`

### Brukerregistrering
1. Gå til `http://localhost:3000/registrer`.
2. Fyll ut navn, etternavn, e-post og passord.
3. Klikk på "Registrer".

### Logg inn
1. Gå til `http://localhost:3000/logginn`.
2. Skriv inn e-post og passord.
3. Klikk på "Login".

### Spill
1. Naviger til `http://localhost:3001`.
2. Bruk WASD-tastene for å bevege spilleren.
3. Unngå hindringer og samle poeng.
    - katuser og astroider vil skade deg 
    - helse eleksirer vil gi deg et liv 
---

## Funksjonalitet

### Flask-applikasjon
- **Brukerregistrering og innlogging:** Opprett og logg inn med en konto.
- **Bokbestillinger:** Bestill bøker og se tidligere bestillinger.
- **Admin-panel:** Administrer brukere (krever admin-rolle).
- **Global score:** Poeng fra spillet lagres og vises i en global scoreliste.

### Pygbag-spill
- **Spillmekanikk:** Unngå hindringer og samle poeng.
- **Livsystem:** Spilleren har 5 liv.
- **Highscore:** Poeng lagres og vises i global score.

---

## Filstruktur

```
AarsOppgaveKinda/
├── app.py                 # Flask-applikasjonen
├── main.py                # Pygbag-spillet
├── database.py            # Databaseoperasjoner
├── sql-kode.sql           # SQL-skript for å opprette databasen
├── pygame.toml            # Konfigurasjonsfil for Pygbag
├── build/
│   └── web/               # Generert mappe for Pygbag-spillet
│       ├── index.html
│       ├── js/
│       ├── css/
│       └── andre filer...
├── templates/             # HTML-maler for Flask
│   ├── index.html
│   ├── logginn.html
│   ├── admin.html
│   └── andre filer...
├── static/                # CSS og JavaScript for Flask
│   ├── felles.css
│   ├── style2.css
│   └── js/
│       └── script.js
└── requirements.txt       # Avhengigheter for Python
```

---

## Feilsøking

### Flask-applikasjonen starter ikke
- Sørg for at alle nødvendige Python-pakker er installert:
  ```bash
  pip install -r requirements.txt
  ```
- Kontroller at MySQL-databasen er riktig konfigurert.

### Spillet kjører ikke i nettleseren
- Sørg for at Pygbag-spillet er bygget riktig:
  ```bash
  pygbag main.py
  ```
- Kontroller at web-mappen inneholder `index.html` og andre nødvendige filer.

### 404-feil for `.apk`-filen
- Sørg for at `.apk`-filen er plassert i web-mappen.

---

## Kontakt

For spørsmål eller problemer, kontakt Anders Christensen
andersmschristensen@icloud.com.
```
