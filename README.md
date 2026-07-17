# Sudoku – App-Paket

Reine Web-App (HTML/JS), als PWA installierbar und mit Capacitor zu einer
Android-APK verpackbar. Keine Abhängigkeiten zur Laufzeit.

```
sudoku-app/
├─ index.html              # das Spiel (App-Einstieg)
├─ manifest.webmanifest    # App-Metadaten (Name, Icons, Vollbild)
├─ service-worker.js       # Offline-Caching
└─ icons/                  # App-Icons (192/512, maskable, apple-touch)
```

---

## Weg A – Als PWA aufs Gerät (schnellster Weg, kein Play Store)

Eine PWA muss über **HTTPS** ausgeliefert werden, damit „Installieren" angeboten
wird (Ausnahme: `localhost` zum Testen). Ein bloßer Doppelklick auf `index.html`
(file://) reicht **nicht** – der Service-Worker startet dann nicht.

### 1. Lokal testen
```bash
cd sudoku-app
python3 -m http.server 8000
```
Am Rechner: http://localhost:8000 → alles läuft, Service-Worker aktiv.

### 2. Öffentlich hosten (HTTPS, kostenlos)
Ordnerinhalt bei einem der folgenden Dienste als statische Seite ablegen:
- **GitHub Pages** (Repo → Settings → Pages)
- **Netlify** / **Cloudflare Pages** (Ordner reinziehen)

### 3. Auf Tablet/Handy installieren
- **Android (Chrome):** Seite öffnen → Menü ⋮ → „App installieren" /
  „Zum Startbildschirm hinzufügen". Danach eigenes Icon, Vollbild, offline.
- **iOS (Safari):** Teilen-Symbol → „Zum Home-Bildschirm".

---

## Weg B – Echte Android-APK mit Capacitor

Ergebnis: installierbare `.apk` (Sideload) bzw. `.aab` (Play Store).
Die Web-Assets werden **in die App eingebettet** – kein Server nötig, sofort offline.

### Voraussetzungen
- Node.js (LTS)
- JDK 17
- Android Studio (inkl. Android SDK)

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

### App-Icons in der nativen App
Capacitor nutzt eigene Android-Ressourcen. Am einfachsten mit dem Asset-Tool:
```bash
npm install -D @capacitor/assets
# eine Quelldatei icon.png (min. 1024x1024) in resources/ ablegen
npx capacitor-assets generate --android
```

---

## Hinweis zum Offline-Speicher
Der aktuelle Spielstand wird noch nicht gespeichert. Wenn du magst, lässt sich
`localStorage` ergänzen, damit ein laufendes Spiel App-Neustarts übersteht.
