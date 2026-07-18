# Sudoku

Web-basiertes Sudoku mit Generator, Notizen, Tipp-Funktion und Offline-Modus.
Reines HTML/CSS/JavaScript ohne Laufzeit-Abhängigkeiten — läuft als Website,
installierbare PWA (Handy/Tablet) und als eigenständige Windows-App.

**Live-Version:** https://goldenexperience96.github.io/sudoku-app/
**Repository:** https://github.com/GoldenExperience96/sudoku-app

---

## Features

- Sudoku-Generator mit eindeutiger Lösung (Backtracking-Solver), vier
  Schwierigkeitsgrade (Leicht/Mittel/Schwer/Experte)
- Bleistift-Notizen pro Zelle, Tipp-Funktion, unbegrenztes Zurück (Undo)
- Zeit- und Fehler-Zähler, Gewinn-Dialog
- Fehler-Erkennung (falsche Ziffern werden rot markiert)
- Helles/dunkles Design, folgt automatisch der Systemeinstellung des Geräts
  (`prefers-color-scheme`)
- Vollständig per Tastatur bedienbar (Pfeiltasten, Ziffern 1–9, Entf, N)
- Offline-fähig via Service-Worker (Cache-first), installierbar als PWA
- Auf dem Handy öffnet ein Zellen-Tap zusätzlich die native Zifferntastatur
  des Geräts

---

## Projektstruktur

```
sudoku-app/
├─ index.html              # das Spiel: Markup, Styles und komplette Spiellogik
├─ manifest.webmanifest    # PWA-Metadaten (Name, Icons, Vollbild, Farben)
├─ service-worker.js       # Offline-Caching (Cache-first, siehe unten)
├─ icons/                  # App-Icons (192/512, maskable, apple-touch, favicon)
├─ make_icons.py           # Skript zur Icon-Generierung aus einer Quellgrafik
├─ desktop/                # Windows-Desktop-App (Electron), siehe unten
│  ├─ main.js              # Electron-Hauptprozess, lädt ../index.html im Fenster
│  ├─ package.json         # Abhängigkeiten + Build-Skripte
│  └─ dist/                # Build-Ausgabe (SudokuApp.exe), nicht in Git
└─ README.md
```

---

## Steuerung

| Eingabe                          | Wirkung                                  |
|-----------------------------------|-------------------------------------------|
| Klick/Tap auf Zelle               | Zelle auswählen (öffnet auf dem Handy zusätzlich die native Zifferntastatur) |
| Ziffer 1–9 (Klick, Tastatur, Handy-Tastatur) | Zahl setzen bzw. im Notizmodus Notiz ein-/austragen |
| Pfeiltasten                       | Auswahl bewegen                          |
| Entf / Rücktaste                  | Zelle leeren                             |
| N                                 | Notizmodus umschalten                    |
| „✏️ Notizen“ / „⌫ Löschen“ / „💡 Tipp“ / „↶ Zurück“ | entsprechende Aktion als Button |

---

## Lokale Entwicklung

Kein Build-Schritt nötig. Da der Service-Worker nur über `http(s)://`
funktioniert (nicht über `file://`), lokal über einen simplen Webserver
öffnen, z. B. mit Node:

```bash
npx serve -l 8000
```

oder mit Python:

```bash
python -m http.server 8000
```

Dann `http://localhost:8000` im Browser öffnen.

### Änderungen veröffentlichen

Der Service-Worker cached alle Assets beim ersten Besuch und beim ihm bereits
bekannte Wiederbesuch **immer aus dem Cache**. Nach jeder inhaltlichen
Änderung an `index.html`, `manifest.webmanifest` oder den Icons deshalb die
Cache-Version in `service-worker.js` hochzählen:

```js
const CACHE = 'sudoku-v5';   // hochzählen, sonst sehen Nutzer die Änderung nicht
```

Danach committen und pushen — GitHub Pages baut die Live-Version automatisch
neu:

```bash
git add -A
git commit -m "..."
git push
```

---

## Als PWA installieren (Handy/Tablet)

Die Live-Version läuft bereits über HTTPS auf GitHub Pages, also direkt
installierbar:

- **Android (Chrome):** https://goldenexperience96.github.io/sudoku-app/
  öffnen → Menü ⋮ → „App installieren“ / „Zum Startbildschirm hinzufügen“
- **iOS (Safari):** Seite öffnen → Teilen-Symbol → „Zum Home-Bildschirm“

Danach: eigenes App-Icon, Vollbild ohne Browserleiste, offline nutzbar.

### Wie das Hosting eingerichtet wurde (zur Referenz)

1. Git + GitHub-CLI (`gh`) installiert, `gh auth login`
2. `git init`, `git add -A`, `git commit`
3. `gh repo create sudoku-app --public --source=. --remote=origin --push`
4. GitHub Pages aktiviert über
   `gh api repos/GoldenExperience96/sudoku-app/pages -X POST -f "source[branch]=main" -f "source[path]=/"`

---

## Windows-Desktop-App (Electron)

Im Ordner [`desktop/`](desktop/) liegt eine dünne Electron-Hülle, die
`index.html` unverändert in einem eigenen Fenster lädt (keine Code-Dopplung,
kein Server nötig).

### Voraussetzungen
- Node.js (LTS)

### Im Entwicklungsmodus starten
```bash
cd desktop
npm install
npm start
```

### Portable EXE bauen
```bash
cd desktop
npm run package:win
```
Ergebnis: `desktop/dist/SudokuApp-win32-x64/SudokuApp.exe` (~260 MB, weil
Chromium/Node mitgeliefert werden). Es ist eine **portable App, kein
Installer** — der komplette Ordner muss zusammenbleiben, wenn er kopiert
oder weitergegeben wird (z. B. als ZIP). Einfach `SudokuApp.exe` per
Doppelklick starten, keine Installation nötig.

`desktop/dist/` und `desktop/node_modules/` sind über `.gitignore` bewusst
vom Repository ausgeschlossen (zu groß fürs Git-Repo).

### Eigenes App-Icon / echter Installer (optional, noch nicht umgesetzt)
- Icon: `.ico`-Datei erzeugen (z. B. mit `png-to-ico`) und in
  `electron-packager` per `--icon=pfad.ico` einbinden
- Installer mit Startmenü-Eintrag statt portablem Ordner: `electron-builder`
  mit NSIS-Target verwenden

---

## Optional: Echte Android-APK mit Capacitor (noch nicht umgesetzt)

Alternative zur PWA, falls später eine `.apk`/`.aab` fürs Sideloading oder
den Play Store gebraucht wird. Die Web-Assets werden dabei in die App
eingebettet — kein Server nötig, sofort offline.

### Voraussetzungen
- Node.js (LTS), JDK 17, Android Studio (inkl. Android SDK)

### Schritte
```bash
# 1. Projekt anlegen
mkdir sudoku-native && cd sudoku-native
npm init -y
npm install @capacitor/core @capacitor/android
npm install -D @capacitor/cli

# 2. Capacitor initialisieren
#    App-Name: Sudoku   |   App-ID: com.deinname.sudoku (umgekehrte Domain)
npx cap init "Sudoku" "com.deinname.sudoku" --web-dir=www

# 3. Web-App einlegen: den Inhalt von sudoku-app/ nach www/ kopieren
#    (index.html, manifest.webmanifest, service-worker.js, icons/)
mkdir www
cp -r ../sudoku-app/* www/

# 4. Android-Plattform hinzufügen und synchronisieren
npx cap add android
npx cap sync

# 5. In Android Studio öffnen und bauen (APK/AAB über Build > Build Bundle(s)/APK(s))
npx cap open android
```

Zum Signieren/Veröffentlichen erzeugst du in Android Studio einen Keystore
(Build > Generate Signed Bundle / APK). Für den Play Store lädst du die
signierte `.aab` in der Play Console hoch.

Für App-Icons in der nativen App eignet sich `@capacitor/assets`:
```bash
npm install -D @capacitor/assets
# eine Quelldatei icon.png (min. 1024x1024) in resources/ ablegen
npx capacitor-assets generate --android
```

---

## Bekannte Lücke

Der Spielstand wird aktuell **nicht** gespeichert. Ein Neuladen der Seite
oder ein Neustart der App beginnt ein neues Spiel. Ließe sich mit
`localStorage` nachrüsten, damit ein laufendes Spiel App-Neustarts übersteht.
